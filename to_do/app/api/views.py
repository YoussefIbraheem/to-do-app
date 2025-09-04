from django.utils.decorators import method_decorator
from app.serializers import ToDoSerializer, CategorySerializer, UserSerializer
from app.models import ToDo, Category
from rest_framework.views import APIView
from rest_framework import permissions, decorators, viewsets
from rest_framework.response import Response
from app.utils import AuthUtils
from drf_yasg.utils import swagger_auto_schema
from .swagger_schemas import login_schema, register_schema , category_list_schema

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


# Category List View

class CategoryList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(**category_list_schema())
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# ToDo ViewSet

class ToDoViewSet(viewsets.ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionError(
                "You do not have permission to delete this ToDo item."
            )
