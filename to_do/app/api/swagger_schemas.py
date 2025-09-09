from drf_yasg import openapi
from app.serializers import UserSerializer
from app.models import ToDo


class AuthSchema:
    def login_schema():
        return {
            "method": "post",
            "operation_description": "Login a user",
            "request_body": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["username", "password"],
                properties={
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Username"
                    ),
                    "password": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Password"
                    ),
                },
            ),
            "responses": {200: openapi.Response("Login successful", UserSerializer)},
        }

    def register_schema():
        return {
            "method": "post",
            "operation_description": "Register a new user",
            "request_body": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["username", "email", "password"],
                properties={
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Username"
                    ),
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Email"
                    ),
                    "password": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Password"
                    ),
                },
            ),
            "responses": {
                200: openapi.Response("Registration successful", UserSerializer)
            },
        }


class CategorySchema:
    def category_list_schema():
        return {
            "operation_description": "Retrieve all categories for the authenticated user",
            "responses": {200: openapi.Response("List of categories")},
        }


class ToDoSchema:

    def todo_list_schema():
        return {
            "operation_description": "Retrieve all todo for the authenticated user",
            "manual_parameters": [
                openapi.Parameter(
                    name="category",
                    in_=openapi.IN_QUERY,
                    type=openapi.TYPE_INTEGER,
                    description="Filter todos by category ID",
                )
            ],
            "responses": {200: openapi.Response("List of todos")},
        }

    def todo_details_schema():
        return {
            "operation_description": "Retrieve a single todo for the authenticated user",
            "responses": {200: openapi.Response("a todo detail")},
        }

    def create_todo_schema():
        return {
            "operation_description": "Create a new todo",
            "request_body": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["title", "description"],
                properties={
                    "title": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Title of the todo"
                    ),
                    "description": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Description of the todo"
                    ),
                    "status": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=ToDo.StatusChoices.values,
                        description="status of the todo",
                        default=ToDo.StatusChoices.PENDING.value,
                    ),
                    "categories": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_INTEGER),
                        description="List of category IDs associated with the todo",
                    ),
                },
            ),
            "responses": {201: openapi.Response("Todo created successfully")},
        }

    def update_todo_schema():
        return {
            "operation_description": "Update an existing todo",
            "request_body": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "title": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Title of the todo"
                    ),
                    "description": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Description of the todo"
                    ),
                    "status": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=ToDo.StatusChoices.choices,
                        description="status of the todo",
                        default=ToDo.StatusChoices.PENDING.value,
                    ),
                    "categories": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_INTEGER),
                        description="List of category IDs associated with the todo",
                    ),
                },
            ),
            "responses": {200: openapi.Response("Todo updated successfully")},
        }

    def delete_todo_schema():
        return {
            "operation_description": "Delete an existing todo",
            "responses": {204: openapi.Response("Todo deleted successfully")},
        }
