from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Category , ToDo
from django.contrib.auth.models import User
from .serializers import CategorySerializer , ToDoSerializer , CreateToDoSerializer
class AuthUtils:

    def login(request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return user, token
        return None, None

    def register(request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        if User.objects.filter(username=username).exists():
            return None, None
        user = User.objects.create_user(username=username, email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return user, token 
    

class CategoryUtils:
    
    def get_categories():
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return serializer
        

class ToDoUtils:
    
    def get_todos(user:User,categories: list[int|None]):
        query = ToDo.objects.filter(user=user)
        if categories:
            query = query.filter(categories__in=categories)
        todos = query.all()
        serializer = ToDoSerializer(todos, many=True)
        return serializer
    
    def create_todo(todo_data, user):
        serializer = CreateToDoSerializer(data=todo_data)
        if serializer.is_valid():
            serializer.save(user=user)
            return serializer
        raise Exception(serializer.error_messages)