from rest_framework import serializers

from .models.Project import Project
from .models.Task import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'project': {'required': True},
            'name': {'required': True},
            'description': {'required': False},
            'status': {'required': True},
            'priority': {'required': True},
            'assignee': {'required': False},
        }


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': False},
        }
