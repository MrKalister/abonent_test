from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    """If not username not raise ValueError."""

    def _create_user(self, username, email, password, **extra_fields):
        """Create and save a user with email, and password."""

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        if username:
            username = GlobalUserModel.normalize_username(username)
            user = self.model(username=username, email=email, **extra_fields)
            user.password = make_password(password)
            user.save(using=self._db)
        else:
            user = self.model(email=email, **extra_fields)
            user.password = make_password(password)
            user.save(using=self._db)
            user.username = 'user ' + str(user.id)
            user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        """The function has changed parameters."""

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
            self, email, username=None, password=None, **extra_fields):
        """The function has changed parameters."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model."""

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        blank=True,
        null=True,
        unique=True,
        validators=[AbstractUser.username_validator]
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
