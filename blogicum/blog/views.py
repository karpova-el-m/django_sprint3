import sys

from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Category, Post

sys.path.append("..")
from blogicum.constants import NOW, POSTS_NUMBER

# Posts = Post.active_posts.valid()
Posts = Post.objects.select_related('category', 'location').filter( 
    pub_date__lte=NOW, 
    is_published=True, 
    category__is_published=True, 
) 


def index(request):
    return render(
        request,
        'blog/index.html',
        {'post_list': Posts[:POSTS_NUMBER]}
    )


def post_detail(request, pk):
    post_detail = get_object_or_404(
        Posts,
        pk=pk
    )
    return render(
        request,
        'blog/detail.html',
        {'post': post_detail}
    )


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    # Я не смогла разобраться, как сослаться на related_name.
    # Если я пишу category.categories.all() - через точечную нотацию -
    # categories не распознаются
    # Может быть я забываю про какой-то импорт?
    post_list = get_list_or_404(Posts.filter(category=category))
    # Если убираю get_list_or_404 - не проходит тест.
    # 'Убедитесь, что страница категории, снятой с публикации, возвращает статус 404.'
    return render(
        request,
        'blog/category.html',
        {'post_list': post_list, 'category': category}
    )
