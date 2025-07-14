from django.urls import path

from .views import generate_bill_details


urlpatterns = [
    # path('', TeacherListView.as_view(), name='teacher_list'),
    path('generate_docx/', generate_bill_details, name='generate_docx'),
]