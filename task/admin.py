from django.contrib import admin
from .models.Project import Project
from .models.Task import Task

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
