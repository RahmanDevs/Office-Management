from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from docxtpl import DocxTemplate
import os
import uuid
from datetime import date

from teachers.models import Teacher
from .models import ExamCommittee, Program,ExamCommitteeMember, AcademicYear
from .models import Course
# Create your views here.

def get_exam_committee(request):
    if request.method == 'GET':
        academic_year = request.GET.get('academic_year', None)
        academic_year_obj=AcademicYear.objects.filter(year=academic_year).first()
        # if academic year does not exists send JsonResponse with Code and message
        if not academic_year_obj:
            return JsonResponse({'code':404, 'message':'Academic Year not found'}, status=404)
        if academic_year_obj:
            committees = ExamCommittee.objects.filter(program__academic_year=academic_year_obj)
            # sorted by program and academic year
            ordered_committees=committees.order_by('program__title_en','program__academic_year__year')
            # return Committee Titles and PK as response
            committee_info = [f"{committee.pk}: {committee.title_en}" for committee in ordered_committees]
            return JsonResponse({'code':200, 'data': committee_info}, status=200)
        


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
    template_path = os.path.join(settings.BASE_DIR, 'templates/doc_file', 'Duty Roster.docx')
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

@csrf_exempt
def generate_exam_resulation(request):
    if request.method == 'POST':
        print("POST request received")
        import json
        data = json.loads(request.body)
        academic_year = data.get('academic_year')
        exam_committee_id = data.get('exam_committee')
        semester = data.get('semester')
        exam_type = data.get('exam_type')
        print(f"Data received: {data}")



        # Fetch the exam committee
        exam_committee = ExamCommittee.objects.filter(id=exam_committee_id).first()
        if not exam_committee:
            return JsonResponse({'error': 'Exam Committee not found'}, status=404)

        # Prepare context for the document
        committee_members = ExamCommitteeMember.objects.filter(committee=exam_committee)
        exam_commitee_chairman = committee_members.filter(role='chairman').first()
        courses=Course.objects.filter(syllabus__program=exam_committee.program)

        # Define context (dynamic data)

        context = {
            'committee_members': committee_members,
            'committee_chairman': exam_commitee_chairman.teacher.full_name_ansi if exam_commitee_chairman else 'N/A',
            'academic_year': academic_year,
            'semester': semester,
            'exam_type': exam_type,
            'courses': courses,
            'question_submission_deadline': data.get('question_submission_deadline', 'N/A'),
            'question_modaration_date': data.get('question_moderation_date', 'N/A'),
            'viva_date_1': data.get('viva_date_1', 'N/A'),
            'viva_date_2': data.get('viva_date_2', 'N/A'),
            'duty_roster_made_by': data.get('duty_roster_made_by', 'N/A'),
        }

        # Load and render the document
        if exam_type == 'regular':
            if semester == '1st':
                template_path = os.path.join(settings.BASE_DIR, 'templates/doc_file', 'Exam Resulation-1.docx')
            else:
                template_path = os.path.join(settings.BASE_DIR, 'templates/doc_file', 'Exam Resulation-1.docx')
        else:
            template_path = os.path.join(settings.BASE_DIR, 'templates/doc_file', 'Exam Resulation-1.docx')  # Use a different template for other exam types if needed
        doc = DocxTemplate(template_path)
        doc.render(context)

        # Generate a unique file name and save the output
        file_name = f"exam_resulation_{uuid.uuid4().hex}.docx"
        output_path = os.path.join(settings.MEDIA_ROOT, file_name)
        doc.save(output_path)

        # Serve the generated file as a download
        with open(output_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
    


    web_context = {
        'academic_years': AcademicYear.objects.all(),
        'semesters': [choice[0] for choice in Course._meta.get_field('semester').choices],
        'teachers': Teacher.objects.all(),
    }
    return render(request, 'exams/Exam Resulation-1.html', web_context)
