from django.urls import path, include
from rest_framework import permissions
from app.api.views import login , register , ToDoList , CategoryList , ToDoDetails
from drf_yasg.views import get_schema_view
from drf_yasg import openapi




schema_view = get_schema_view(
    openapi.Info(
        title="To-DO API",
        default_version="v1",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "swagger.<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("todos/", ToDoList.as_view(), name="todo-list"),
    path("todos/<int:pk>", ToDoDetails.as_view(), name="todo-details")
]
