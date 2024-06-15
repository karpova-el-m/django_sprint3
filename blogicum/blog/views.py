from django.shortcuts import render, get_object_or_404, get_list_or_404
from blog.models import Post, Category
from datetime import datetime

Posts = Post.objects.select_related('category', 'location').filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    post_list = Posts.order_by('-pub_date')
    context = {'post_list': post_list[0:5]}
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    post_detail = get_object_or_404(Posts, pk=pk)
    context = {'post': post_detail}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.filter(slug=category_slug))
    post_list = get_list_or_404(Posts.filter(category=category))
    context = {'post_list': post_list, 'category': category}
    return render(request, 'blog/category.html', context)
