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

    def validate(self, attrs):
        request = self.context.get('request')
        print('context:', request.method)
        if request and request.method == 'POST':
            if not Project.objects.filter(id = attrs.get('id', None)).exists():
                raise serializers.ValidationError("Project with this ID not exists.")
            if not attrs.get('title', None):
                raise serializers.ValidationError("Project title is required.")
        elif request and request.method in ['PATCH', 'PUT']:
            print('request method: ', request.method)
            if Project.objects.filter(id = attrs.get('id', None)).exists():
                raise serializers.ValidationError("Project with this ID already exists.")
            if not attrs.get('title', None):
                raise serializers.ValidationError("Project title is required.")
        elif request and request.method == 'GET':
            pass

        return attrs