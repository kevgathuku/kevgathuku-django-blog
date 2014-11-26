from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.utils.html import escape

from blog.views import index, category, contact, show_post
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


class PaginationTest(HomePageTest):
    """Pagination Tests for the Index Page"""

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

    def test_index_page_displays_next_page_link(self):
        PostFactory.reset_sequence()
        posts = PostFactory.create_batch(
            10, published=True, content='some content')

        response = self.client.get('/')

        self.assertContains(response, 'Older Posts')

    def test_next_page_link_not_displayed_if_not_enough_posts(self):
        published = PublishedPostFactory.create()

        response = self.client.get('/')

        self.assertNotContains(response, 'Older Posts')

    def test_previous_page_link_shown_if_enough_posts(self):
        PostFactory.reset_sequence()
        posts = PostFactory.create_batch(
            10, published=True, content='some content')

        response = self.client.get('/?page=2')

        self.assertContains(response, 'Newer Posts')


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
        unpublished = UnPublishedPostFactory.create(category=test_category)
        published = PublishedPostFactory.create(category=test_category)

        response = self.client.get('/category/%s/' % test_category.slug)

        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "My Unpublished Post")

    def test_invalid_category_slug(self):
        response = self.client.get('/category/does-not-exist/')

        self.assertContains(response, 'Error')
        self.assertContains(response, 'The specified category does not exist!')

    def test_empty_category(self):
        test_category = CategoryFactory(name='test category')

        response = self.client.get(
            '/category/{slug}/'.format(slug=test_category.slug))

        self.assertContains(
            response, 'Nothing has been posted in this category yet.')


class CategoryPaginationTest(CategoryTest):
    """Pagination Tests for the Category View"""

    def test_page_number_not_an_integer_redirects_to_category_view(self):
        cat = CategoryFactory()
        published = PublishedPostFactory.create(category=cat)

        response = self.client.get(
            '/category/{slug}/?page=ab'.format(slug=cat.slug))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published Post")

    def test_page_number_out_of_range_redirects_to_last_page(self):
        cat = CategoryFactory()
        PostFactory.reset_sequence()
        posts = PostFactory.create_batch(
            10, published=True, content='content', category=cat)

        response = self.client.get(
            '/category/{slug}/?page=999'.format(slug=cat.slug))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, posts[0].title)
        self.assertNotContains(response, posts[9].title)

    def test_category_view_displays_next_page_link(self):
        cat = CategoryFactory(name='test')
        PostFactory.reset_sequence()
        posts = PostFactory.create_batch(
            10, published=True, content='some content', category=cat)

        response = self.client.get(
            '/category/{slug}/'.format(slug=cat.slug))

        self.assertContains(response, 'Older Posts')

    def test_next_page_link_not_displayed_if_not_enough_posts(self):
        cat = CategoryFactory()
        published = PublishedPostFactory.create(category=cat)

        response = self.client.get('/category/{slug}/'.format(slug=cat.slug))

        self.assertNotContains(response, 'Older Posts')

    def test_previous_page_link_shown_if_enough_posts(self):
        cat = CategoryFactory()
        PostFactory.reset_sequence()
        posts = PostFactory.create_batch(
            10, published=True, content='some content', category=cat)

        response = self.client.get(
            '/category/{slug}/?page=2'.format(slug=cat.slug))

        self.assertContains(response, 'Newer Posts')


class ContactViewTest(TestCase):
    """Tests the Contact View"""

    def post_invalid_input(self):
        return self.client.post(
            '/contact/',
            data={
            'name': '',
            'email': 'me@gmail.com',
            'message': 'message'
                }
        )

    def post_valid_input(self):
        return self.client.post(
            '/contact/',
            data={
            'name': 'Blog Fan',
            'email': 'myemail@email.com',
            'message': 'I am your biggest fan',
                }
            )

    def test_contact_view_resolves_to_correct_view(self):
        cat = resolve('/contact/')
        self.assertEqual(cat.func, contact)

    def test_uses_contact_template(self):
        response = self.client.get('/contact/')
        self.assertTemplateUsed(response, 'blog/contact.html')

    def test_contact_form_has_csrf_token(self):
        response = self.client.get('/contact/')

        self.assertIn('csrfmiddlewaretoken', response.content.decode())

    def test_mail_sent_on_successful_POST_request(self):
        self.post_valid_input()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, '[kevgathuku] Web Contact Form')


class ShowPostTest(TestCase):
    """Test for individual post view"""

    def test_post_url_resolves_to_correct_view(self):
        found = resolve('/post/new/')
        self.assertEqual(found.func, show_post)

    def test_uses_post_template(self):
        published = PublishedPostFactory.create()

        response = self.client.get('/post/{}/'.format(published.slug))
        self.assertTemplateUsed(response, 'blog/post.html')

    def test_show_post_displays_post_content(self):
        published = PublishedPostFactory.create()

        response = self.client.get('/post/{}/'.format(published.slug))

        self.assertContains(response, "Published Post")

    def test_resolves_only_published_posts(self):
        unpublished = UnPublishedPostFactory.create()
        published = PublishedPostFactory.create()

        response = self.client.get('/post/{}/'.format(published.slug))
        bad_response = self.client.get('/post/{}/'.format(unpublished.slug))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bad_response.status_code, 404)
