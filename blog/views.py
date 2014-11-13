from django.shortcuts import render, get_object_or_404
from django.views import generic

from blog.models import Post, Category


class ListPosts(generic.ListView):
    context_object_name="posts"
    paginate_by = 5
    allow_empty = True


class IndexView(ListPosts):
    template_name = 'blog/index.html'

    def get_queryset(self):
        """Return the last five published posts."""
        return Post.objects.filter(published=True).order_by('-created')


class CategoryView(ListPosts):
    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'],published=True).order_by('-created')


class ShowPost(generic.DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get_object(self):
        return get_object_or_404(Post.objects.filter(slug=self.kwargs['slug'],published=True))


def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')
