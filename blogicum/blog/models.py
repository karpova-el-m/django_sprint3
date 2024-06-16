import sys

from django.contrib.auth import get_user_model
from django.db import models

from core.models import BaseModel

sys.path.append("..")
from blogicum.constants import MAX_LENGTH, MAX_NAME_LENGTH, NOW

User = get_user_model()

# class PostsManager(models.Manager):
#     def valid(self):
#         return self.filter(
#             pub_date__lte=NOW,
#             is_published=True,
#             category__is_published=True,
#         )


class Location(BaseModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название места'
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return (
            self.name if len(self.name) <= MAX_NAME_LENGTH
            else f'{self.name[:MAX_NAME_LENGTH]}...'
        )


class Category(BaseModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return (
            self.title if len(self.title) <= MAX_NAME_LENGTH
            else f'{self.title[:MAX_NAME_LENGTH]}...'
        )
    

class Post(BaseModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        editable=True,
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем '
            '— можно делать отложенные публикации.'
        ),
    )
    # active_posts = PostsManager()
    # Если здесь переопределяю objects = PostsManager(),
    # То во views Post.objects.valid() не работает -
    # не распознает objects через точечную нотацию.
    # Post.active_posts.valid() - работает.
    # Но не проходит 2 теста - Post has no attribute 'objects'.
    # Как быть в этом случае?
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        related_name = 'locations',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='categories',
        null=True,
        verbose_name='Категория',
    )


    class Meta(BaseModel.Meta):
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return (
            self.title if len(self.title) <= MAX_NAME_LENGTH
            else f'{self.title[:MAX_NAME_LENGTH]}...'
        )
    
