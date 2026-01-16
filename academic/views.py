from django.shortcuts import render

from django.http import HttpResponse
from django.conf import settings
from docxtpl import DocxTemplate
import os
import uuid
from datetime import date
from .models import ExamCommittee, Program
from .models import Course
# Create your views here.

def get_yearly_courses_code(request):
    if request.method == 'GET':
        academic_year = request.GET.get('academic_year', None)
        semester = request.GET.get('semester', None)
        program= request.GET.get('program', None)
        if academic_year and semester and program:
            courses = Course.objects.filter(
                syllabus__program__academic_year__year=academic_year,
                semester=semester,
                syllabus__program__title_en=program
            )
            course_codes = [course.course_code for course in courses]
            return HttpResponse(', '.join(course_codes))

def get_program(request):
    if request.method == 'GET':
        academic_year = request.GET.get('academic_year', None)
        if academic_year:
            programs = Program.objects.filter(academic_year__year=academic_year)
            program_titles = [program.title_en for program in programs]
            return HttpResponse(', '.join(program_titles))

def generate_bill_details(request):
    # Load the template
    template_path = os.path.join(settings.BASE_DIR, 'templates/doc_file', 'Bill Details.docx')
    doc = DocxTemplate(template_path)
    exam_committee = ExamCommittee.objects.first()  # Get the first exam committee for demonstration

    # Define context (dynamic data)
    context = {
        'class': 'we.wU.AvB.Gm. ¯œvZK (m¤§vb) 3q el©',
        'semester': '2q',
        'year': exam_committee.year,
        'session': exam_committee.session,
        'chairman': exam_committee.chairman.full_name_ansi,
        'members': [member.full_name_ansi for member in exam_committee.member.all()],
        'external_member': exam_committee.external_member if exam_committee.external_member else 'N/A',  #full_name_ansi
        'date': date.today().strftime('%Y-%m-%d'),
    }
    print(context)

    # Render the template with the context
    doc.render(context)

    # Generate a unique file name and save the output
    file_name = f"generated_{uuid.uuid4().hex}.docx"
    output_path = os.path.join(settings.MEDIA_ROOT, file_name)
    doc.save(output_path)

    # Serve the generated file as a download
    with open(output_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
