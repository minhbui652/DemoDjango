from django.core.serializers import serialize
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models.Assign import Assign
from .models.Project import Project
from .models.Task import Task
from .serializers import ProjectSerializer, TaskSerializer
from django.core.paginator import Paginator
from django.db.models import Q

'''
CRUD Project với function-based view (FBV)
'''
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_all(request):
    try:
        project = Project.objects.filter(
            Q(title__icontains=request.query_params.get('keyword', '')) |
            Q(description__icontains=request.query_params.get('keyword', ''))
        ).all()

        page_size = int(request.query_params.get('page_size', 10))  # Mặc định là 2 items mỗi trang
        p = Paginator(project, page_size)
        page_number = request.query_params.get('page', 1)
        result = p.get_page(page_number)
        serializer = ProjectSerializer(result, many=True, context={'request': request})
        response = {
            'count': p.count,
            'total_pages': p.num_pages,
            'current_page': result.number,
            'page_size': page_size,
            'results': serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})

@api_view(['GET'])
def get_by_id(request, id):
    try:
        if type(id) != int:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid ID format'})
        query = Project.objects.get(id=id)
        serializer = ProjectSerializer(query, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        print('type id la: ', type(id))
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Project not found'})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    try:
        print(request.data)
        serialize = ProjectSerializer(data=request.data, context={'request': request})
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request):
    try:
        query = Project.objects.get(id=request.data['id'])
        serializer = ProjectSerializer(query, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request, id):
    try:
        query = Project.objects.get(id=id)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Project not found'})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})

# sử dụng các hàm trong django để lấy dữ liệu
@api_view(['GET'])
def getAssigned(request, id):
    try:
        project = Project.objects.get(id=id)
        if project is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Project not found'})
        assigns = Assign.objects.select_related('user', 'project').filter(project=project, isDeleted=False).all()
        response = [
            {
                'projectId': assign.project_id,
                'userId': assign.user_id,
                'userName': assign.user.username,
                'projectTitle': assign.project.title,
            } for assign in assigns
        ]
        return Response(response, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Project not found'})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})

# Sử dụng truy vấn SQL để lấy dữ liệu
@api_view(['GET'])
def getTask(request, id):
    try:
        project = Project.objects.get(id=id)
        if project is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Project not found'})

        query = Task.objects.raw('SELECT * FROM Task WHERE Task.project_id = %s', [project.id])
        response = [
            {
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'deadline': task.deadline
            } for task in query
        ]
        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})

'''
CRUD TASK với class base view (APIView)
'''
class TaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})

    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
            if task is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Task not found'})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})

    def post(self, request):
        try:
            serialize = TaskSerializer(data=request.data)
            print('serialize: ', serialize)
            if serialize.is_valid():
                serialize.save()
                return Response(serialize.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid data', 'serialize': serialize.errors})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e), 'data': request.data})

    def put(self, request):
        try:
            task = Task.objects.get(id=request.data['id'])
            if task is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serialize = TaskSerializer(task, data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response(serialize.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid data', 'serialize': serialize.errors})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e), 'serialize': serialize.errors})

    def patch(self, request, id):
        try:
            task = Task.objects.get(id=id)
            if task is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid data', 'serializer': serializer.errors})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})

    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
            if task is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Task not found'})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})