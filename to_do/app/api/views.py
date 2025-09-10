from django.utils.decorators import method_decorator
from app.serializers import (
    ToDoSerializer,
    CategorySerializer,
    UserSerializer,
    CreateToDoSerializer,
)
from app.models import ToDo, Category
from rest_framework.views import APIView
from rest_framework import permissions, decorators, viewsets, status
from rest_framework.response import Response
from app.utils import AuthUtils
from drf_yasg.utils import swagger_auto_schema
from .swagger_schemas import AuthSchema, CategorySchema, ToDoSchema
from django.views.decorators.cache import cache_page

# Authentication


@swagger_auto_schema(**AuthSchema.login_schema())
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def login(request):
    user, token = AuthUtils.login(request)
    if user is not None:
        return Response({"user": UserSerializer(user).data, "token": token.key})
    else:
        return Response({"error": "Invalid Credentials"}, status=400)


@swagger_auto_schema(**AuthSchema.register_schema())
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def register(request):
    user, token = AuthUtils.register(request)
    if user is not None:
        return Response({"user": UserSerializer(user).data, "token": token.key})
    else:
        return Response({"error": "Username already exists"}, status=400)


# Category List View


class CategoryList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(**CategorySchema.category_list_schema())
    @method_decorator(cache_page(60 * 15, key_prefix="category_list"))
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# ToDo List
class ToDoList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**ToDoSchema.todo_list_schema())
    @method_decorator(cache_page(60 * 15, key_prefix="todo_list"))
    def get(self,request: dict, format=None):
        todo = ToDo.objects.filter(user=request.user)
        if 'categories' in request.query_params:
            categories = request.query_params.getlist('categories', [])
            todo = todo.filter(categories__in=categories)
        serializer = ToDoSerializer(todo, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**ToDoSchema.create_todo_schema())
    def post(self, request, format=None):
        serializer = CreateToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(**ToDoSchema.update_todo_schema())
    def put(self, request, pk, format=None):
        to_do = self.get_object(pk)
        serializer = CreateToDoSerializer(to_do, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(**ToDoSchema.delete_todo_schema())
    def delete(self, request, pk, format=None):
        to_do = self.get_object(pk)
        to_do.delete()
        return Response(status=204)


class ToDoDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return ToDo.objects.filter(user=request.user).get(pk=pk)
        except ToDo.DoesNotExist as e:
            raise Exception("ToDo not found") from e
    @swagger_auto_schema(**ToDoSchema.todo_details_schema())
    def get(self, request, pk, format=None):
        to_do = self.get_object(request, pk)
        serializer = ToDoSerializer(to_do)
        return Response(serializer.data)
