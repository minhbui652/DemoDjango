"""
URL configuration for TaskManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from task.views import get_all, get_by_id, create, update, delete, getAssigned, getTask, TaskAPIView
from user.views import UserViewSet, AssignViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('assign', AssignViewSet, basename='assign')

urlpatterns = [
    # project api using function-based view
    path('admin/', admin.site.urls),
    path('api/project/getAll', get_all),
    path('api/project/getById/<int:id>', get_by_id),
    path('api/project/create', create),
    path('api/project/update', update),
    path('api/project/delete/<int:id>', delete),
    path('api/project/getAssigned/<int:id>', getAssigned),
    path('api/project/getTask/<int:id>', getTask),
    path('api/task', TaskAPIView.as_view(), name='task-list'),
    path('api/task/<int:id>', TaskAPIView.as_view(), name='task-detail'),
    path('api/', include(router.urls))
]
