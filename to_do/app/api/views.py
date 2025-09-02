from app.serializers import ToDoSerializer, CategorySerializer, UserSerializer
from app.models import ToDo, Category
from django.contrib.auth.models import User
from rest_framework import permissions , decorators
from rest_framework.response import Response


@decorators.api_view(['GET' , 'POST'])
def category_list(request):
    
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)