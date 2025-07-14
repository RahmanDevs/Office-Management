from django.urls import path

from .views import TeacherListView, FacultyListView


urlpatterns = [
    path('', TeacherListView.as_view(), name='teacher_list'),
    path('faculty/', FacultyListView.as_view(), name='faculty_list'),
]