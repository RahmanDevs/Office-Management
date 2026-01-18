from django.urls import path

from .views import generate_bill_details, get_program, get_yearly_courses_code,generate_exam_resulation, get_exam_committee


urlpatterns = [
    # path('', TeacherListView.as_view(), name='teacher_list'),
    path('generate_docx/', generate_bill_details, name='generate_docx'),
    path('get_yearly_courses_code/', get_yearly_courses_code, name='get_yearly_courses_code'), # URL: /academic/get_yearly_courses_code/?admission_session=2023-2024&semester=1st&program=Computer%20Science%20and%20Engineering
    path('get_program/', get_program, name='get_program'), # URL: /academic/get_program/?academic_year=2023
    path('get_exam_committee/', get_exam_committee, name='get_exam_committee'), # URL: /academic/get_exam_committee/?academic_year=2023
    path('generate-exam-resulation',generate_exam_resulation, name="generate_exam_resulation" )
]