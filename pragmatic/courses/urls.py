from django.urls import path

from lessons import views as lessons_views

from . import views

app_name = 'courses'

urlpatterns = [
    path(
        'category/',
        views.CategoryListView.as_view(),
        name='category_list',
    ),
    path(
        'category/<slug:slug>/',
        views.CategoryDetailView.as_view(),
        name='category_detail',
    ),
    path('', views.CourseListView.as_view(), name='index'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path(
        '<int:pk>/lesson/',
        lessons_views.LessonCreateView.as_view(),
        name='create_lesson',
    ),
    path(
        '<int:pk>/lesson/<int:lesson_id>/edit/',
        lessons_views.LessonUpdateView.as_view(),
        name='edit_lesson',
    ),
    path(
        '<int:pk>/lesson/<int:lesson_id>/delete/',
        lessons_views.LessonDeleteView.as_view(),
        name='delete_lesson',
    ),
]
