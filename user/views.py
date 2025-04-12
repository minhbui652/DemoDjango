# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models.User import User
from .serializers import UserSerializer, AssignSerializer, CustomTokenObtainPairSerializer
from rest_framework import permissions
from .models.Assign import Assign
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

class AuthViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        if User.objects.filter(username=request.data['username']).exists():
            user = User.objects.get(username=request.data['username'])
            if user.check_password(request.data['password']):
                # cấp token
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'message': 'Login successful',
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'is_staff': user.is_staff,
                        }
                     }
                )
            else:
                return Response({'error': 'Invalid password'}, status=400)
        else:
            return Response({'error': 'User not found'}, status=404)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    def list(self, request, *args, **kwargs):
        """
        Override list method to add custom permission check
        """
        self.check_permissions(request)
        response = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            } for user in self.queryset
        ]
        return Response(response)

    def create(self, request, *args, **kwargs):
        query = User.objects.filter(username=request.data['username'])
        if query.exists():
            return Response({'error': 'Username already exists'}, status=400)
        data = request.data.copy()
        data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(data=data, context={'request': request})

        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=400)  # Trả về lỗi nếu dữ liệu không hợp lệ

        serializer.save()
        return Response(serializer.data, status=201)

class AssignViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Assign.objects.all()
    serializer_class = AssignSerializer
    permission_classes = [permissions.IsAuthenticated]
