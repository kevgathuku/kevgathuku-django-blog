from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from blog.views import IndexView
from .factories import *


class HomePageTest(TestCase):

    def test_root_url_resolves_to_correct_view(self):
        found = resolve('/')
        self.assertEqual(found.view_name, 'home')

    def test_uses_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        expected_html = render_to_string('blog/index.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_displays_only_published_items(self):
        unpublished = UnPublishedPostFactory.create()
        published = PublishedPostFactory.create()

        response = self.client.get('/')

        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "My Unpublished Post")
