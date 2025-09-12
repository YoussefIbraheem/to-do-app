# api/test.py
from django.urls import reverse
from rest_framework.test import (
    APITestCase,
    APIClient,
    APIRequestFactory,
    force_authenticate,
)
from rest_framework import status
from django.contrib.auth.models import User
from app.models import ToDo, Category
from app.api.views import ToDoList, ToDoDetails


class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_register_user(self):
        url = reverse("register")
        data = {"username": "newuser", "password": "newpass"}
        response = self.client.post(url, data, format="json")
        # your register view returns 200 on success in previous code; adjust if yours returns 201
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_register_existing_user(self):
        url = reverse("register")
        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_valid_credentials(self):
        url = reverse("login")
        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_invalid_credentials(self):
        url = reverse("login")
        data = {"username": "wronguser", "password": "wrongpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CategoryTests(APITestCase):
    def setUp(self):
        Category.objects.create(name="Work")
        Category.objects.create(name="Personal")

    def test_category_list(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ToDoTests(APITestCase):
    """
    Mix of integration tests (APIClient + reverse) and unit-ish view tests
    (APIRequestFactory + direct view call). The detail/update/delete tests
    below show the usage of APIRequestFactory and how to pass `pk` properly.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # APIClient is convenient for higher-level tests (routing, etc.)
        self.client = APIClient()
        # keep client authenticated for integration tests
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Work")
        self.todo = ToDo.objects.create(
            title="Test ToDo", description="Description", user=self.user
        )
        self.todo.categories.add(self.category)

    # # ------- Integration-style tests using APIClient + reverse() -------
    # def test_get_todos_list_integration(self):
    #     url = reverse("todo-list")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)

    # def test_create_todo_integration(self):
    #     url = reverse("todo-list")
    #     data = {
    #         "title": "New ToDo",
    #         "description": "Test desc",
    #         "categories": [self.category.id],
    #     }
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data["title"], "New ToDo")

    # # If reverse with args is giving trouble, try kwargs:
    # def test_reverse_with_kwargs_example(self):
    #     # reverse using kwargs instead of args
    #     url = reverse("to-do-details", kwargs={"pk": self.todo.id})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ------- View-level tests using APIRequestFactory (explicit pk) -------
    def test_get_todo_details_via_factory(self):
        """
        Show how to call the view directly and pass pk as a keyword arg.
        This is useful when you want to test the view logic in isolation.
        """
        request = self.factory.get(f"/todos/{self.todo.id}")
        force_authenticate(request, user=self.user)
        view = ToDoDetails.as_view()
        response = view(request, pk=self.todo.id)
        # DRF Response objects produced by view(...) might need rendering to access .data
        if hasattr(response, "render"):
            response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test ToDo")

    def test_update_todo_via_factory(self):
        request = self.factory.put(
            f"/todos/{self.todo.id}",
            {
                "title": "Updated ToDo",
                "description": "Updated desc",
                "categories": [self.category.id],
            },
            format="json",
        )
        force_authenticate(request, user=self.user)
        view = ToDoDetails.as_view()
        response = view(request, pk=self.todo.id)
        if hasattr(response, "render"):
            response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated ToDo")

    def test_delete_todo_via_factory(self):
        request = self.factory.delete(f"/todos/{self.todo.id}")
        force_authenticate(request, user=self.user)
        view = ToDoDetails.as_view()
        response = view(request, pk=self.todo.id)
        # DELETE often returns 204 and may not have .data; render is still safe
        if hasattr(response, "render"):
            response.render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ToDo.objects.filter(id=self.todo.id).exists())

    def test_get_non_existent_todo_via_factory(self):
        request = self.factory.get("/todos/999")
        force_authenticate(request, user=self.user)
        view = ToDoDetails.as_view()
        response = view(request, pk=999)
        if hasattr(response, "render"):
            response.render()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_todo_list_via_factory(self):
        # Don't authenticate -> should be 401 for IsAuthenticated view
        unauth_request = self.factory.get("/todos/")
        view = ToDoList.as_view()
        response = view(unauth_request)
        if hasattr(response, "render"):
            response.render()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
