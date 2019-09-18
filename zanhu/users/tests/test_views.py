from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model

from zanhu.users.views import UserDetailView, UserUpdateView

User = get_user_model()


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User(username="testuser", password="password")


class UserUpdateTestCase(BaseUserTestCase):

    def setUp(self):
        super().setUp()
        self.view = UserUpdateView()
        request = self.factory.get('/')
        request.user = self.user
        self.view.request = request

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), '/users/testuser/')

    def test_get_object(self):
        self.assertEqual(self.view.get_object(), self.user)

