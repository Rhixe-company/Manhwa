from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField, BooleanField, ImageField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from .managers import UserManager


def user_image_location(instance, filename):
    return "{}/{}".format(
        str(instance.email)
        .replace(" ", "_")
        .replace(":", " ")
        .replace("/", "")
        .replace("\\", ""),
        filename,
    )


ext_validator = FileExtensionValidator(
    ["ico", "png", "jpg", "svg", "jpeg", "gif", "webp", "ttf", "eot", "woff", "woff2"]
)


class User(AbstractUser):
    """
    Default custom user model for Rhixe Scans.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    # name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("First Name of User"), blank=True, max_length=255)  # type: ignore[assignment]
    last_name = CharField(_("Last Name of User"), blank=True, max_length=255)  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = CharField(_("User Name"), unique=True, max_length=2550)
    images = ImageField(
        _("Images"),
        upload_to=user_image_location,
        validators=[ext_validator],
        default="/images/user.png",
    )
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects: ClassVar[UserManager] = UserManager()

    def delete(self, *args, **kwargs):
        self.images.delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def update_absolute_url(self) -> str:
        return reverse("users:update-user", kwargs={"pk": self.id})

    def delete_absolute_url(self) -> str:
        return reverse("users:delete-user", kwargs={"pk": self.id})
