from django.db import models
from django.urls import reverse

from courses.models import Course


class Lesson(models.Model):
    class LessonType(models.TextChoices):
        EDU = 'edu', 'Программирование'
        THEORY = 'theory', 'Теория'
        QUIZ = 'quiz', 'Викторина'

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    type = models.CharField(max_length=16, verbose_name='Тип урока', choices=LessonType.choices)
    duration = models.PositiveSmallIntegerField(
        verbose_name='Продолжительность',
        help_text='Укажите продолжительность курса в минутах.'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Отредактировано')

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lessons:lesson_detail', args=(self.pk,))
