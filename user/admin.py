from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.Assign import Assign
from .models.User import User

# Register your models here.
admin.site.register(User)
admin.site.register(Assign)
