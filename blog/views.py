from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Category


def index(request):
    """The home page view. Returns the last five published posts."""

    context = {}
    page = request.GET.get('page', 1)
    index_queryset = Post.objects.filter(published=True).order_by('-created')
    paginator = Paginator(index_queryset, 5)

    try:
        posts = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    context['posts'] = posts

    return render(request, 'blog/index.html', context)


def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        
        context_dict['category_name'] = category.name
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        cat_posts = Post.objects.filter(category=category,published=True).order_by('-created')

        # Adds our results list to the template context under name pages.
        context_dict['posts'] = cat_posts

        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'blog/category.html', context_dict)


class ShowPost(generic.DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get_object(self):
        return get_object_or_404(Post.objects.filter(slug=self.kwargs['slug'],published=True))


def about(request):
    return render(request, 'blog/about.html')

def about_site(request):
    return render(request, 'blog/about-this-site.html')

def contact(request):
    return render(request, 'blog/contact.html')
