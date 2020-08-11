from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

from datetime import date


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)  # new user model
        user.set_password(password)
        user.save(using=self.db)  # supports multiple databases

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Album(models.Model):
    """Album Object"""
    name = models.CharField(max_length=400)
    release_date = models.DateField(default=date.today)
    artist = models.CharField(max_length=255)
    # Image Field
    # album_cover = models.ImageField(blank=True, null=True, upload_to='covers/')
    cover = models.ImageField(blank=True, null=True, upload_to='covers/')
    album_link = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return self.name
