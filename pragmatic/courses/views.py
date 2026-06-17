from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

from .models import Category, Course


def visible_courses(queryset, user):
    """Аноним видит только публичные курсы, авторизованный — все."""
    if not user.is_authenticated:
        queryset = queryset.filter(is_public=True)
    return queryset


class CategoryListView(ListView):
    model = Category
    template_name = 'courses/category_list.html'


class CategoryDetailView(SingleObjectMixin, ListView):
    template_name = 'courses/category_detail.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.object.course_set.select_related(
            'author', 'category',
        ).order_by('-created_at')
        return visible_courses(queryset, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context


class CourseListView(ListView):
    template_name = 'courses/index.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = Course.objects.select_related(
            'author', 'category',
        ).order_by('-created_at')
        return visible_courses(queryset, self.request.user)


class CourseDetailView(DetailView):
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_queryset(self):
        queryset = Course.objects.select_related('author', 'category')
        return visible_courses(queryset, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = self.object.lesson_set.all()
        return context
