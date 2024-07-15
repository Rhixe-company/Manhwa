import os
from typing import Any, Dict, List, Optional

from django.contrib.auth import get_user_model

import fido2.features
from fido2.server import Fido2Server
from fido2.utils import websafe_decode, websafe_encode
from fido2.webauthn import (
    AttestedCredentialData,
    AuthenticationResponse,
    AuthenticatorData,
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
    RegistrationResponse,
    UserVerificationRequirement,
)

from allauth.account.utils import url_str_to_user_pk
from allauth.core import context
from allauth.mfa import app_settings
from allauth.mfa.adapter import get_adapter
from allauth.mfa.models import Authenticator


from typing import Callable, Optional

from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.authentication import record_authentication
from allauth.core import context, ratelimit
from allauth.mfa import signals
from allauth.mfa.models import Authenticator

import binascii
import hmac
import os
import struct
from hashlib import sha1
from typing import List, Optional

from allauth.mfa import app_settings
from allauth.mfa.models import Authenticator
from allauth.mfa.utils import decrypt, encrypt


class RecoveryCodes:
    def __init__(self, instance: Authenticator) -> None:
        self.instance = instance

    @classmethod
    def activate(cls, user) -> "RecoveryCodes":
        instance = Authenticator.objects.filter(
            user=user, type=Authenticator.Type.RECOVERY_CODES
        ).first()
        if instance:
            return cls(instance)
        instance = Authenticator(
            user=user,
            type=Authenticator.Type.RECOVERY_CODES,
            data={
                "seed": encrypt(cls.generate_seed()),
                "used_mask": 0,
            },
        )
        instance.save()
        return cls(instance)

    @classmethod
    def generate_seed(self) -> str:
        key = binascii.hexlify(os.urandom(20)).decode("ascii")
        return key

    def _get_migrated_codes(self) -> Optional[List[str]]:
        codes = self.instance.data.get("migrated_codes")
        if codes is not None:
            return [decrypt(code) for code in codes]
        return None

    def generate_codes(self) -> List[str]:
        migrated_codes = self._get_migrated_codes()
        if migrated_codes is not None:
            return migrated_codes

        ret = []
        seed = decrypt(self.instance.data["seed"])
        h = hmac.new(key=seed.encode("ascii"), msg=None, digestmod=sha1)
        for i in range(app_settings.RECOVERY_CODE_COUNT):
            h.update((f"{i:3},").encode("utf-8"))
            value = struct.unpack(">I", h.digest()[:4])[0]
            value %= 10**8
            fmt_value = f"{value:08}"
            ret.append(fmt_value)
        return ret

    def _is_code_used(self, i: int) -> bool:
        used_mask = self.instance.data["used_mask"]
        return bool(used_mask & (1 << i))

    def _mark_code_used(self, i: int) -> None:
        used_mask = self.instance.data["used_mask"]
        used_mask |= 1 << i
        self.instance.data["used_mask"] = used_mask
        self.instance.save()

    def get_unused_codes(self) -> List[str]:
        migrated_codes = self._get_migrated_codes()
        if migrated_codes is not None:
            return migrated_codes

        ret = []
        for i, code in enumerate(self.generate_codes()):
            if self._is_code_used(i):
                continue
            ret.append(code)
        return ret

    def _validate_migrated_code(self, code: str) -> Optional[bool]:
        migrated_codes = self._get_migrated_codes()
        if migrated_codes is None:
            return None
        try:
            idx = migrated_codes.index(code)
        except ValueError:
            return False
        else:
            migrated_codes = self.instance.data["migrated_codes"]
            assert isinstance(migrated_codes, list)
            migrated_codes.pop(idx)
            self.instance.data["migrated_codes"] = migrated_codes
            self.instance.save()
            return True

    def validate_code(self, code: str) -> bool:
        ret = self._validate_migrated_code(code)
        if ret is not None:
            return ret

        for i, c in enumerate(self.generate_codes()):
            if self._is_code_used(i):
                continue
            if code == c:
                self._mark_code_used(i)
                return True
        return False


def delete_dangling_recovery_codes(user) -> Optional[Authenticator]:
    deleted_authenticator = None
    qs = Authenticator.objects.filter(user=user)
    if not qs.exclude(type=Authenticator.Type.RECOVERY_CODES).exists():
        deleted_authenticator = qs.first()
        qs.delete()
    return deleted_authenticator


def delete_and_cleanup(request, authenticator) -> None:
    authenticator.delete()
    rc_auth = delete_dangling_recovery_codes(authenticator.user)
    for auth in [authenticator, rc_auth]:
        if auth:
            signals.authenticator_removed.send(
                sender=Authenticator,
                request=request,
                user=request.user,
                authenticator=auth,
            )


def post_authentication(
    request,
    authenticator: Authenticator,
    reauthenticated: bool = False,
    passwordless: bool = False,
) -> None:
    authenticator.record_usage()
    extra_data = {
        "id": authenticator.pk,
        "type": authenticator.type,
    }
    if reauthenticated:
        extra_data["reauthenticated"] = True
    if passwordless:
        extra_data["passwordless"] = True
    record_authentication(request, "mfa", **extra_data)


def check_rate_limit(user) -> Callable[[], None]:
    key = f"mfa-auth-user-{str(user.pk)}"
    if not ratelimit.consume(
        context.request,
        action="login_failed",
        key=key,
    ):
        raise get_account_adapter().validation_error("too_many_login_attempts")
    return lambda: ratelimit.clear(context.request, action="login_failed", key=key)


if not fido2.features.webauthn_json_mapping.enabled:
    fido2.features.webauthn_json_mapping.enabled = True


CHALLENGE_SESSION_KEY = "mfa.webauthn.challenge"
STATE_SESSION_KEY = "mfa.webauthn.state"
EXTENSIONS = {"credProps": True}


def build_user_payload(user) -> PublicKeyCredentialUserEntity:
    kwargs = get_adapter().get_public_key_credential_user_entity(user)
    return PublicKeyCredentialUserEntity(**kwargs)


def generate_challenge() -> bytes:
    challenge = context.request.session.get(CHALLENGE_SESSION_KEY)
    if challenge is not None:
        return websafe_decode(challenge)
    challenge = os.urandom(32)
    context.request.session[CHALLENGE_SESSION_KEY] = websafe_encode(challenge)
    return challenge


def consume_challenge() -> None:
    context.request.session.pop(CHALLENGE_SESSION_KEY, None)


def get_state() -> Optional[Dict]:
    return context.request.session.get(STATE_SESSION_KEY)


def set_state(state: Dict) -> None:
    context.request.session[STATE_SESSION_KEY] = state


def clear_state() -> None:
    context.request.session.pop(STATE_SESSION_KEY, None)


def get_server() -> Fido2Server:
    rp_kwargs = get_adapter().get_public_key_credential_rp_entity()
    rp = PublicKeyCredentialRpEntity(**rp_kwargs)
    verify_origin = None
    if app_settings.WEBAUTHN_ALLOW_INSECURE_ORIGIN:
        verify_origin = lambda o: True  # noqa
    server = Fido2Server(rp, verify_origin=verify_origin)
    return server


def parse_registration_response(response: Any) -> RegistrationResponse:
    try:
        return RegistrationResponse.from_dict(response)
    except TypeError:
        raise get_adapter().validation_error("incorrect_code")


def begin_registration(user) -> Dict:
    server = get_server()
    credentials = get_credentials(user)
    registration_data, state = server.register_begin(
        user=build_user_payload(user),
        credentials=credentials,
        user_verification=UserVerificationRequirement.DISCOURAGED,
        challenge=generate_challenge(),
        extensions=EXTENSIONS,
    )
    set_state(state)
    return dict(registration_data)


def complete_registration(credential: Dict) -> AuthenticatorData:
    server = get_server()
    state = get_state()
    if not state:
        raise get_adapter().validation_error("incorrect_code")
    binding = server.register_complete(state, credential)
    consume_challenge()
    clear_state()
    return binding


def get_credentials(user) -> List[AttestedCredentialData]:
    credentials: List[AttestedCredentialData] = []
    authenticators = Authenticator.objects.filter(
        user=user, type=Authenticator.Type.WEBAUTHN
    )
    for authenticator in authenticators:
        credential_data = authenticator.wrap().authenticator_data.credential_data
        if credential_data:
            credentials.append(authenticator.wrap().authenticator_data.credential_data)
    return credentials


def get_authenticator_by_credential_id(
    user, credential_id: bytes
) -> Optional[Authenticator]:
    authenticators = Authenticator.objects.filter(
        user=user, type=Authenticator.Type.WEBAUTHN
    )
    for authenticator in authenticators:
        if (
            credential_id
            == authenticator.wrap().authenticator_data.credential_data.credential_id
        ):
            return authenticator
    return None


def parse_authentication_response(response: Any) -> AuthenticationResponse:
    try:
        return AuthenticationResponse.from_dict(response)
    except TypeError:
        raise get_adapter().validation_error("incorrect_code")


def begin_authentication(user=None) -> Dict:
    server = get_server()
    request_options, state = server.authenticate_begin(
        credentials=get_credentials(user) if user else [],
        user_verification=UserVerificationRequirement.PREFERRED,
        challenge=generate_challenge(),
    )
    set_state(state)
    return dict(request_options)


def extract_user_from_response(response: Dict):
    try:
        user_handle = response.get("response", {}).get("userHandle")
        user_pk = url_str_to_user_pk(websafe_decode(user_handle).decode("utf8"))
    except (ValueError, TypeError, KeyError):
        raise get_adapter().validation_error("incorrect_code")
    user = get_user_model().objects.filter(pk=user_pk).first()
    if not user:
        raise get_adapter().validation_error("incorrect_code")
    return user


def complete_authentication(user, response: Dict) -> Authenticator:
    credentials = get_credentials(user)
    server = get_server()
    state = get_state()
    if not state:
        raise get_adapter().validation_error("incorrect_code")
    try:
        binding = server.authenticate_complete(state, credentials, response)
    except ValueError as e:
        # ValueError: Unknown credential ID.
        raise get_adapter().validation_error("incorrect_code") from e
    consume_challenge()
    clear_state()
    authenticator = get_authenticator_by_credential_id(user, binding.credential_id)
    if not authenticator:
        raise get_adapter().validation_error("incorrect_code")
    return authenticator


class WebAuthn:
    def __init__(self, instance):
        self.instance = instance

    @classmethod
    def add(cls, user, name: str, credential: dict) -> "WebAuthn":
        instance = Authenticator(
            user=user,
            type=Authenticator.Type.WEBAUTHN,
            data={
                "name": name,
                "credential": credential,
            },
        )
        instance.save()
        return cls(instance)

    @property
    def name(self) -> str:
        return self.instance.data["name"]

    @name.setter
    def name(self, name: str):
        self.instance.data["name"] = name

    @property
    def authenticator_data(self) -> AuthenticatorData:
        return parse_registration_response(
            self.instance.data["credential"]
        ).response.attestation_object.auth_data

    @property
    def is_passwordless(self) -> Optional[bool]:
        return (
            self.instance.data.get("credential", {})
            .get("clientExtensionResults", {})
            .get("credProps", {})
            .get("rk")
        )
