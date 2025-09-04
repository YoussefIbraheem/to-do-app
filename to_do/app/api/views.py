from app.serializers import ToDoSerializer, CategorySerializer, UserSerializer
from app.models import ToDo, Category
from rest_framework import permissions, decorators
from rest_framework.response import Response
from app.utils import AuthUtils
from drf_yasg.utils import swagger_auto_schema
from .swagger_schemas import login_schema , register_schema

# Authentication

@swagger_auto_schema(**login_schema())
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def login(request):
    user, token = AuthUtils.login(request)
    if user is not None:
        return Response({"user": UserSerializer(user).data, "token": token.key})
    else:
        return Response({"error": "Invalid Credentials"}, status=400)


@swagger_auto_schema(**register_schema())
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def register(request):
    user, token = AuthUtils.register(request)
    if user is not None:
        return Response({"user": UserSerializer(user).data, "token": token.key})
    else:
        return Response({"error": "Username already exists"}, status=400)
