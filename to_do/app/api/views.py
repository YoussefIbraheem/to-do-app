from app.serializers import ToDoSerializer, CategorySerializer, UserSerializer
from app.models import ToDo, Category
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework import permissions, decorators
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Authentication
@swagger_auto_schema(
    method="post",
    operation_description="Login a user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username", "password"],
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password"),
        },
    ),
    responses={200: openapi.Response("Login successful", UserSerializer)},
)
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"user": UserSerializer(user).data, "token": token.key})
    else:
        return Response({"error": "Invalid Credentials"}, status=400)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def register(request):
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)
    user = User.objects.create_user(username=username, email=email, password=password)
    token = Token.objects.get_or_create(user=user)
    return Response({"user": UserSerializer(user).data, "token": token.key})
