from allauth.account.forms import (
    AddEmailForm,
    ChangePasswordForm,
    LoginForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SetPasswordForm,
    SignupForm,
)
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.socialaccount.forms import DisconnectForm
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.utils.safestring import mark_safe
from allauth.utils import set_form_field_order
from django.contrib.auth import get_user_model, password_validation

from allauth.mfa.forms import AuthenticateForm, ActivateTOTPForm, DeactivateTOTPForm


User = get_user_model()


class UserAdminForm(forms.ModelForm):

    captcha = ReCaptchaField(
        # widget=ReCaptchaV2Checkbox(
        #     attrs={
        #         "data-theme": "dark",
        #         # "data-size": "compact",
        #     }
        # )
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "images",
            "is_staff",
            "is_superuser",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-charinput", "placeholder": _("User Name")}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-charinput", "placeholder": _("admin@test.com")}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-charinput", "placeholder": _("First Name")}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-charinput", "placeholder": _("Last Name")}
            ),
            # "images": forms.FileInput(
            #     attrs={
            #         "class": "form-charinput file-input file-input-bordered ",
            #         "placeholder": _("Images"),
            #     }
            # ),
        }

    def clean_username(self):
        return self.cleaned_data["username"].strip()

    def clean_email(self):
        if self.cleaned_data["email"] == "":
            self.add_error("email", 'The field "Email" is required.')
        else:
            return self.cleaned_data["email"].strip()


class UserForm(forms.ModelForm):

    captcha = ReCaptchaField(
        # widget=ReCaptchaV2Checkbox(
        #     attrs={
        #         "data-theme": "dark",
        #         # "data-size": "compact",
        #     }
        # )
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-charinput",
                "autocomplete": "current-password",
                "placeholder": _("••••••••"),
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-charinput",
                "placeholder": _("••••••••"),
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "images",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-charinput", "placeholder": _("User Name")}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-charinput", "placeholder": _("admin@test.com")}
            ),
            # "images": forms.FileInput(
            #     attrs={
            #         "class": "form-charinput file-input file-input-bordered ",
            #         "placeholder": _("Images"),
            #     }
            # ),
        }

    def clean_username(self):
        return self.cleaned_data["username"].strip()

    def clean_email(self):
        if self.cleaned_data["email"] == "":
            self.add_error("email", 'The field "Email" is required.')
        else:
            return self.cleaned_data["email"].strip()

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")
        if password != confirm_password:
            self.add_error("password1", "Password and confirm password does not match.")
        return cleaned_data


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):

    images = forms.ImageField(label=_("Images"))
    # captcha = CaptchaField(
    #     label=_("Captcha"),
    #     help_text=_("Enter the Letters Above."),
    #     widget=CaptchaTextInput(
    #         attrs={
    #             "class": "form-charinput",
    #         }
    #     ),
    # )
    captcha = ReCaptchaField(
        # widget=ReCaptchaV2Checkbox(
        #     attrs={
        #         "data-theme": "dark",
        #         # "data-size": "compact",
        #     }
        # )
    )
    forgot_txt = _("Terms and Conditions")
    remember = forms.BooleanField(
        label="Terms",
        required=True,
        help_text=mark_safe(
            f"<label for='terms' class='font-medium text-gray-900 dark:text-white'   > I accept the <a class='text-primary-700 hover:underline dark:text-primary-500' href='/#/'>{forgot_txt}</a></label>"
        ),
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-checkbox",
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-charinput",
                "hx-post": reverse_lazy("users:check-email"),
                "hx-trigger": "keyup[target.value.length    >   6]    changed delay:3s",
                "hx-swap": "afterend",
                "hx-target": "#id_email",
                "placeholder": _("name@rhixe.company"),
                "autocomplete": "email",
            }
        ),
    )
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(
            attrs={
                "class": "form-charinput",
                "hx-post": reverse_lazy("users:check-username"),
                "hx-trigger": "keyup[target.value.length    >   3]    changed delay:3s",
                "hx-swap": "afterend",
                "hx-target": "#id_username",
                "placeholder": _("User Name"),
                "autocomplete": "username",
            }
        ),
    )
    first_name = forms.CharField(
        label=_("First Name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-charinput",
                "placeholder": _("First Name"),
                "autocomplete": "first_name",
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-charinput",
                "placeholder": _("Last Name"),
                "autocomplete": "last_name",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UserSignupForm, self).__init__(*args, **kwargs)
        password1_widget = forms.PasswordInput(
            attrs={
                "class": "form-charinput",
                "autocomplete": "password1",
                "placeholder": _("••••••••"),
            }
        )
        password1_field = forms.CharField(
            label=_("Password"),
            strip=False,
            help_text=password_validation.password_validators_help_text_html(),
            widget=password1_widget,
        )
        self.fields["password1"] = password1_field
        password2_widget = forms.PasswordInput(
            attrs={
                "class": "form-charinput",
                "autocomplete": "password2",
                "placeholder": _("••••••••"),
            }
        )
        password2_field = forms.CharField(
            label=_("Password Confirmation"),
            strip=False,
            help_text=_("Enter the same password as before, for verification."),
            widget=password2_widget,
        )
        self.fields["password2"] = password2_field
        set_form_field_order(
            self,
            [
                "email",
                "username",
                "first_name",
                "last_name",
                "images",
                "terms",
                "captcha",
                "password1",
                "password2",
            ],
        )

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.images = self.cleaned_data["images"]
        print(user.images)
        user.save()
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class MyCustomLoginForm(LoginForm):
    # captcha = CaptchaField(
    #     label=_("Captcha"),
    #     widget=CaptchaTextInput(
    #         attrs={
    #             "class": "form-charinput",
    #         }
    #     ),
    # )

    captcha = ReCaptchaField(
        # widget=ReCaptchaV2Checkbox(
        #     attrs={
        #         "data-theme": "dark",
        #         # "data-size": "compact",
        #     }
        # )
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-charinput",
                "autocomplete": "password",
                "placeholder": _("••••••••"),
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-checkbox",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        login_widget = forms.EmailInput(
            attrs={
                "class": "form-charinput",
                "placeholder": _("name@company.com"),
                "autocomplete": "email",
            }
        )
        login_field = forms.EmailField(label=_("Email"), widget=login_widget)
        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])

    def login(self, *args, **kwargs):

        # Add your own processing here.

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)


class MyCustomAddEmailForm(AddEmailForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns an allauth.account.models.EmailAddress object.
        email_address_obj = super(MyCustomAddEmailForm, self).save(request)

        # Add own processing here.

        # You must return the original result.
        return email_address_obj


class MyCustomChangePasswordForm(ChangePasswordForm):

    def save(self):

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(MyCustomChangePasswordForm, self).save()

        # Add own processing here.


class MyCustomSetPasswordForm(SetPasswordForm):

    def save(self):

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(MyCustomSetPasswordForm, self).save()

        # Add own processing here.


class MyCustomResetPasswordForm(ResetPasswordForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a string containing the email address supplied
        email_address = super(MyCustomResetPasswordForm, self).save(request)

        # Add own processing here.

        # Ensure you return the original result
        return email_address


class MyCustomResetPasswordKeyForm(ResetPasswordKeyForm):

    def save(self):

        # Add own processing here.

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(MyCustomResetPasswordKeyForm, self).save()


class MyCustomSocialDisconnectForm(DisconnectForm):
    def save(self):
        # Add own processing here if you do need access to the
        # socialaccount being deleted.

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(MyCustomSocialDisconnectForm, self).save()

        # Add own processing here if you don't need access to the
        # socialaccount being deleted.


class MyCustomAuthenticateForm(AuthenticateForm):
    pass


class MyCustomActivateTOTPForm(ActivateTOTPForm):
    pass


class MyCustomDeactivateTOTPForm(DeactivateTOTPForm):
    pass
