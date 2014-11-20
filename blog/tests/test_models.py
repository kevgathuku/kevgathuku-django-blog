from django.test import TestCase

from .factories import *


class BlogPostTest(TestCase):

    def test_get_absolute_url(self):
        test_post = PostFactory()
        self.assertEqual(
            test_post.get_absolute_url(),
            '/post/{0}/'.format(test_post.slug))
