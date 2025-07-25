from django.urls import path
from . import views



urlpatterns = [
    
    # path('', TeacherListView.as_view(), name='teacher_list'),
    path("exam-duty-roster/", views.generate_duty_roster_docx, name="exam_duty_roster"),
    path('exam-bill-notesheet/', views.generate_exam_bill_notesheet, name='exam_bill_notesheet')

]

