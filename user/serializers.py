from typing import Any

from rest_framework import serializers
from .models.User import User
from .models.Assign import Assign
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'is_active': {'required': False},
            'is_staff': {'required': False},
        }

    def validate(self, attrs):
        """
        Validate email format
        """
        print('context: ', self.context)  # Kiểm tra context

        email = attrs.get('email')
        request = self.context.get('request')  # Lấy request từ context

        # Kiểm tra nếu là POST
        if request and request.method == 'POST':
            # Kiểm tra email đã tồn tại trong cơ sở dữ liệu chưa
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email already exists.")
            # Kiểm tra xem email có hợp lệ không
            if not email or '@' not in email:
                raise serializers.ValidationError("Email is required and must be valid.")

        # Kiểm tra nếu là PUT hoặc PATCH
        elif request and request.method in ['PUT', 'PATCH']:
            if not email or '@' not in email:
                raise serializers.ValidationError("Email is required and must be valid.")

        return attrs

class AssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assign
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'required': True},
            'project': {'required': True},
        }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['is_staff'] = self.user.is_staff
        return data