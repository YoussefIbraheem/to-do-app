from .models import Category, ToDo
from django.contrib.auth.models import User
from . import faker


class ToDoFactory:

    def create(self, **kwargs):
        return {
            "title": kwargs.get("title", faker.word()),
            "description": kwargs.get("description", faker.paragraph(5)),
            "status": kwargs.get(
                "status",
                faker.random_element(elements=[choice[0] for choice in ToDo.StatusChoices.choices]),
            ),
        }


class CategoryFactory:
    
    def create(self, **kwargs):
        return {"name": kwargs.get("namr", faker.word())}


class UserFactory:
    
    def create(self, **kwargs):
        return {
            "username": kwargs.get("username", faker.user_name()),
            "email": kwargs.get("email", faker.unique.email()),
            "password": kwargs.get("password", "password123"),
            "first_name": kwargs.get("first_name", faker.first_name()),
            "last_name": kwargs.get("last_name", faker.last_name()),
        }