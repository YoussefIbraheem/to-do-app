from rest_framework import serializers
from app.models import ToDo, Category
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ToDoSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = ToDo
        fields = "__all__"


class CreateToDoSerializer(serializers.ModelSerializer):
    
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True , required=False)
  
    class Meta:
        model = ToDo
        exclude = ['id' , 'user']

    def create(self, validated_data):
        todo = ToDo.objects.create(
            title = validated_data["title"],
            description = validated_data.get("description", ""),
            status = validated_data.get("status", ToDo.StatusChoices.PENDING),
            user = validated_data["user"],
        )
        todo.categories.set(validated_data["categories"])
        return todo
