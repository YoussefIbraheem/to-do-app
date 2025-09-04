from django.urls import path, include
from rest_framework.routers import DefaultRouter , SimpleRouter
from rest_framework import permissions
from app.api.views import login , register , ToDoViewSet , CategoryList 
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

simple_router = SimpleRouter()

simple_router.register(r"todos", ToDoViewSet, basename="todo")


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
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
    path("", include(simple_router.urls)),
]
