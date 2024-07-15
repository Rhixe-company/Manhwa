from django.contrib.auth.hashers import PBKDF2PasswordHasher
import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class MyPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    """
    A subclass of PBKDF2PasswordHasher that uses 1 iteration.

    This is for test purposes only. Never use anywhere else.
    """

    iterations = 1


class CustomStorage(FileSystemStorage):
    """Custom storage for django_ckeditor_5 images."""

    location = os.path.join(settings.MEDIA_ROOT, "upload")
    base_url = urljoin(settings.MEDIA_URL, "upload/")
