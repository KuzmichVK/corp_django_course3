from django.urls import path

from . import views

app_name = 'lessons'

urlpatterns = [
    path('<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]
