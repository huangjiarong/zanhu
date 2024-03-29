from django.urls import reverse, resolve
from django.test import TestCase


class TestUsersUrls(TestCase):

    def test_update_reverse(self):
        self.assertEqual(reverse('users:update'), '/users/update/')

    def test_update_resolve(self):
        self.assertEqual(resolve('/users/update/').view_name, 'users:update')

    def test_detail_reverse(self):
        self.assertEqual(reverse('users:detail', kwargs={'username': 'testuser'}), '/users/testuser/')

    def test_detail_resolve(self):
        self.assertEqual(resolve('/users/testuser/').view_name, 'users:detail')
