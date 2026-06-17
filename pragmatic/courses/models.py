from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:category_detail', args=(self.slug,))


class Course(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор курса',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичный',
        help_text='Установите галочку, чтобы сделать курс публичным.',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Отредактировано')

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course_detail', args=(self.pk,))
