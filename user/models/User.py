# Create your models here.
from django.contrib.auth.base_user import BaseUserManager

from Utils.models.TimeStampedModel import TimeStampedModel
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def active(self):
        return self.filter(is_active=True)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'User'

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name