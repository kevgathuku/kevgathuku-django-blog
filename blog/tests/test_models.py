from django.test import TestCase

from .factories import *


class BlogPostTest(TestCase):

    def test_get_absolute_url(self):
        test_post = PostFactory()
        self.assertEqual(
            test_post.get_absolute_url(),
            '/post/{0}/'.format(test_post.slug))

    def test_unicode_representation(self):
        test_post = PostFactory()
        self.assertEqual(
            test_post.__unicode__(),
            '{0}'.format(test_post.title))


class CategoryTest(TestCase):

    def test_get_absolute_url(self):
        test_cat = CategoryFactory()
        self.assertEqual(
            test_cat.get_absolute_url(),
            '/category/{0}/'.format(test_cat.slug))

    def test_unicode_representation(self):
        test_uni = CategoryFactory()
        self.assertEqual(
            test_uni.__unicode__(),
            '{0}'.format(test_uni.name))
