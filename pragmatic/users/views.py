from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from courses.models import Course

User = get_user_model()


class UserRegistrationCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')


class UserProfileDetailView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        courses = Course.objects.filter(
            author=self.object,
        ).order_by('-created_at')
        if not self.request.user.is_authenticated:
            courses = courses.filter(is_public=True)
        context['courses'] = courses

        context['courses_count'] = (
            Course.objects.filter(author=self.object)
            .values('is_public')
            .annotate(count=Count('id'))
        )
        return context
