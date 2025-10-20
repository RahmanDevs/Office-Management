from django.urls import path
from . import views



urlpatterns = [
    
    # path('', TeacherListView.as_view(), name='teacher_list'),
    path("exam-duty-roster/", views.generate_duty_roster_docx, name="exam_duty_roster"),
    path('exam-bill-notesheet/', views.generate_exam_bill_notesheet, name='exam_bill_notesheet')

]

from .views import google_sheet_docx_page, generate_docx_from_google_sheet

urlpatterns += [
    path("google-sheet-docx/", google_sheet_docx_page, name="google_sheet_docx_page"),
    path("google-sheet-docx/generate/", generate_docx_from_google_sheet, name="generate_docx_from_google_sheet"),
]