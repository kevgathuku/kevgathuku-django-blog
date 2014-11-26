from django.core.context_processors import csrf
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from .models import Post, Category


def index(request):
    """The home page view. Returns the last five published posts."""

    context = {}
    page = request.GET.get('page', 1)
    index_queryset = Post.objects.filter(published=True).order_by('-created')
    paginator = Paginator(index_queryset, 5, orphans=2)

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
    """The category view. Displays posts under a certain category"""

    context_dict = {}
    page = request.GET.get('page')

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        cat = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        cat_posts = Post.objects.filter(
            category=cat, published=True).order_by('-created')

        paginator = Paginator(cat_posts, 5, orphans=2)

        try:
            posts = paginator.page(page)

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)

        except EmptyPage:
            # If page is out of range (e.g. 999), display last page
            posts = paginator.page(paginator.num_pages)

        context_dict['posts'] = posts

        # Add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = cat

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything. The template displays the error messsage.
        pass

    # Go render the response and return it to the client.
    return render(request, 'blog/category.html', context_dict)


def show_post(request, slug):
    query = Post.objects.filter(slug=slug, published=True)
    post = get_object_or_404(query)

    context = {'post': post}

    return render(request, 'blog/post.html', context)


def about(request):
    return render(request, 'blog/about.html')


def about_site(request):
    return render(request, 'blog/about-this-site.html')


def contact(request):

    context = {}
    context.update(csrf(request))

    if request.method == 'POST':
        name = request.POST.get('name', '')
        message = request.POST.get('message', '')
        from_email = request.POST.get('email', '')
        subject = "[kevgathuku] New Message from {}".format(name)
        if name and message and from_email:
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    ['kevgathuku@gmail.com'],
                    fail_silently=False)
            except BadHeaderError:
                return HttpResponseForbidden(reason='Invalid header found.')
            return JsonResponse({'success': '1'})
        else:
            return HttpResponseForbidden(
                reason='Make sure all fields are entered and valid.')

    return render(request, 'blog/contact.html', context)
