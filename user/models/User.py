# Create your models here.
from Utils.models.TimeStampedModel import TimeStampedModel
from django.db import models

class User(TimeStampedModel):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.username
