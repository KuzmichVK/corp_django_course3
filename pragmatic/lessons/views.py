from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from courses.models import Course
from .models import Lesson

LESSON_FIELDS = ('title', 'text', 'type', 'duration')


class LessonDetailView(DetailView):
    template_name = 'lessons/lesson_detail.html'

    def get_queryset(self):
        queryset = Lesson.objects.select_related('course')
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(course__is_public=True)
        return queryset


class AuthorCourseRequiredMixin(LoginRequiredMixin):
    """Доступ к управлению уроком — только автору курса.

    Аноним перенаправляется на страницу авторизации (LoginRequiredMixin),
    авторизованный не-автор получает 404 на запрашиваемый курс.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.course = get_object_or_404(
                Course, pk=kwargs['pk'], author=request.user,
            )
        return super().dispatch(request, *args, **kwargs)


class LessonCreateView(AuthorCourseRequiredMixin, CreateView):
    model = Lesson
    fields = LESSON_FIELDS
    template_name = 'lessons/lesson_form.html'

    def form_valid(self, form):
        form.instance.course = self.course
        return super().form_valid(form)


class LessonUpdateView(AuthorCourseRequiredMixin, UpdateView):
    model = Lesson
    fields = LESSON_FIELDS
    template_name = 'lessons/lesson_form.html'
    pk_url_kwarg = 'lesson_id'

    def get_queryset(self):
        return Lesson.objects.filter(course=self.course)


class LessonDeleteView(AuthorCourseRequiredMixin, DeleteView):
    model = Lesson
    template_name = 'lessons/lesson_confirm_delete.html'
    pk_url_kwarg = 'lesson_id'

    def get_queryset(self):
        return Lesson.objects.filter(course=self.course)

    def get_success_url(self):
        return reverse('courses:course_detail', args=(self.course.pk,))
