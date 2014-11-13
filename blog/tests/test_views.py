from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from blog.views import IndexView


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

	def test_index_view_with_no_posts(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertIn("Nothing has been posted yet. Thanks for checking in", response.content)
		self.assertQuerysetEqual(response.context['posts'], [])
