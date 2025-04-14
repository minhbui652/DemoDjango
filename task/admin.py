from django.contrib import admin
from .models.Project import Project
from .models.Task import Task

# Register your models here.
admin.site.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'updated_at')
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_staff = request.user.is_staff
        if is_staff:
            print('User is staff', is_staff)
            form.base_fields['title'].disabled = True
            form.base_fields['description'].disabled = True
        else:
            form.base_fields['title'].disabled = False
            form.base_fields['description'].disabled = False
        return form
admin.site.register(Task)
