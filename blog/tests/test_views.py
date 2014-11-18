from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from blog.views import index, category
from .factories import *


class HomePageTest(TestCase):

    def test_root_url_resolves_to_correct_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_uses_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        expected_html = render_to_string('blog/index.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_displays_post_title(self):
        published = PublishedPostFactory.create()

        response = self.client.get('/')

        self.assertContains(response, "Published Post")


    def test_home_page_displays_only_published_items(self):
        unpublished = UnPublishedPostFactory.create()
        published = PublishedPostFactory.create()

        response = self.client.get('/')

        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "My Unpublished Post")

    def test_page_number_not_an_integer_redirects_to_home_page(self):
        published = PublishedPostFactory.create()

        response = self.client.get('/?page=index')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published Post")

    def test_page_number_out_of_range_redirects_to_last_page(self):
        PostFactory.reset_sequence()
        posts = PostFactory.create_batch(10, published=True, content='content')

        response = self.client.get('/?page=999')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, posts[0].title)
        self.assertNotContains(response, posts[9].title)


class CategoryTest(TestCase):

    def test_category_view_resolves_to_correct_view(self):
        cat = resolve('/category/kevin/')
        self.assertEqual(cat.func, category)

    def test_uses_category_template(self):
        response = self.client.get('/category/abcde/')
        self.assertTemplateUsed(response, 'blog/category.html')

    def test_category_view_returns_correct_html(self):
        response = self.client.get('/category/abcde/')
        expected_html = render_to_string('blog/category.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_category_view_displays_only_published_items(self):
        test_category = CategoryFactory(name='test category')
        unpublished = UnPublishedPostFactory.create(category = test_category)
        published = PublishedPostFactory.create(category = test_category)

        response = self.client.get('/category/%s/' % test_category.slug)

        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "My Unpublished Post")

    def test_invalid_category_slug(self):
        response = self.client.get('/category/does-not-exist/')

        self.assertContains(response, 'Error')
        self.assertContains(response, 'The specified category does not exist!')

    def test_empty_category(self):
        test_category = CategoryFactory(name='test category')

        response = self.client.get('/category/{slug}/'.format(slug=test_category.slug))

        self.assertContains(response, 'Nothing has been posted in this category yet. Thanks for checking in')
