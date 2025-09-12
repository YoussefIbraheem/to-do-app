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
from rest_framework.exceptions import APIException, NotAuthenticated
from app.utils import AuthUtils, CategoryUtils, ToDoUtils
from drf_yasg.utils import swagger_auto_schema
from .swagger_schemas import AuthSchema, CategorySchema, ToDoSchema
from django.views.decorators.cache import cache_page
from django.http import Http404

# Authentication


class AuthView:
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
        try:
            serializer = CategoryUtils.get_categories()
            return Response(serializer.data)
        except NotAuthenticated as e:
            raise Response(e.detail, status=status.HTTP_403_FORBIDDEN)


# ToDo List
class ToDoList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**ToDoSchema.todo_list_schema())
    @method_decorator(cache_page(60 * 15, key_prefix="todo_list"))
    def get(self, request, format=None):
        try:
            categories = request.query_params.getlist("categories", [])
            serializer = ToDoUtils.get_todos(request.user, categories)
            return Response(serializer.data)
        except APIException as e:
            raise Response(e.detail, status=e.status_code)

    @swagger_auto_schema(**ToDoSchema.create_todo_schema())
    def post(self, request, format=None):
        try:
            serializer = ToDoUtils.create_todo(request.data, request.user)
            return Response(serializer.data, status=201)
        except APIException as e:
            raise Response(e.detail, status=e.status_code)


class ToDoDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, user, pk):
        try:
            return ToDo.objects.filter(user=user).get(pk=pk)
        except ToDo.DoesNotExist:
            raise Http404

    @swagger_auto_schema(**ToDoSchema.todo_details_schema())
    def get(self, request, pk, format=None):
        print(request.user)
        todo = self.get_object(user=request.user, pk=pk)
        serializer = ToDoSerializer(todo)
        return Response(serializer.data)

    @swagger_auto_schema(**ToDoSchema.update_todo_schema())
    def put(self, request, pk, format=None):
        todo = self.get_object(user=request.user, pk=pk)
        serializer = CreateToDoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(**ToDoSchema.delete_todo_schema())
    def delete(self, request, pk, format=None):
        todo = self.get_object(user=request.user, pk=pk)
        todo.delete()
        return Response(status=204)
