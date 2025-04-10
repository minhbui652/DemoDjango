from django.contrib import admin

from .models.Assign import Assign
from .models.User import User

# Register your models here.
admin.site.register(User)
admin.site.register(Assign)
