from django.test import TestCase

from django.contrib.auth import get_user_model
from zanhu.news.models import News

User = get_user_model()

class NewsTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='password')
        self.user2 = User.objects.create(username='user2', password='password')
        self.news1 = News.objects.create(user=self.user1, content='第一条动态')
        self.news2 = News.objects.create(user=self.user1, content='第二条动态')
        self.news3 = News.objects.create(user=self.user2, content='评论第一条动态',
                                         parent=self.news1, reply=True)

    def test_switch_liked(self):
        """测试点赞或取消赞功能"""
        #user2用户给new1动态点赞
        self.news1.switch_liked(self.user2)
        self.assertEqual(self.news1.count_likers(), 1, msg='点赞失败')
        self.assertIn(self.user2, self.news1.get_likers())
        #user2用户取消赞
        self.news1.switch_liked(self.user2)
        self.assertEqual(self.news1.count_likers(), 0, msg='取消赞失败')
        self.assertNotIn(self.user2, self.news1.get_likers())

    def test_reply_this(self):
        """测试评论功能"""
        #user2用户给new1动态评论
        self.news1.reply_this(self.user2, '评论第一条动态')
        self.assertEqual(self.news1.comment_count(), 2)
        self.assertIn(self.news3, self.news1.get_thread())

    def test_str(self):
        self.assertEqual(self.news1.__str__(), '第一条动态')
