# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from .models.User import User
from .serializers import UserSerializer, AssignSerializer
from rest_framework import permissions
from .models.Assign import Assign

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

class AssignViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Assign.objects.all()
    serializer_class = AssignSerializer
