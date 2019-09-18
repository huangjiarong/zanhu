#!/usr/bin/python
#coding: utf-8

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTestCase(TestCase):

    def setUp(self):
        self.user = User(username="username", password="password")

    def test__str__(self):
        self.assertEqual(self.user.__str__(), 'username')

    def test_get_absoulte_url(self):
        self.assertEqual(self.user.get_absolute_url(), '/users/username/')

    def test_get_profile_name(self):
        self.assertEqual(self.user.get_profile_name(), 'username')
        self.user.nickname = 'nickname'
        self.assertEqual(self.user.get_profile_name(), 'nickname')

    def tearDown(self):
        print("测试函数执行后执行")

# from test_plus.test import TestCase
#
#
# class TestUser(TestCase):
#
#     def setUp(self):
#         self.user = self.make_user()
#
#     def test__str__(self):
#         self.assertEqual(self.user.__str__(), 'testuser')
#
#     def test_get_absoulte_url(self):
#         self.assertEqual(self.user.get_absolute_url(), '/users/testuser/')
#
#     def test_get_profile_name(self):
#         self.assertEqual(self.user.get_profile_name(), 'testuser')
#         self.user.nickname = 'nickname'
#         self.assertEqual(self.user.get_profile_name(), 'nickname')
#

