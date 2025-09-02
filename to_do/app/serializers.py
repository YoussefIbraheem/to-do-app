from rest_framework import serializers
from app.models import ToDo, Category
from django.contrib.auth.models import User


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model=ToDo
        fields='__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email']