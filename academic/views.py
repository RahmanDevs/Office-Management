from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from docxtpl import DocxTemplate
import os
import uuid
from datetime import date, datetime

from teachers.models import Teacher
from .models import ExamCommittee, Program,ExamCommitteeMember, AcademicYear, Course, SEMESTER_CHOICES



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


# Get Bangla day, working function with date_obj or string input also
def get_bangla_day(date_input, lang='bn_ansi'):
    bangla_days_ansi = ['†mvgevi', 'g½jevi', 'eyaevi', 'e„n¯úwZevi', 'ïµevi', 'kwbevi', 'iweevi']
    bangla_days_uni = ['সোমবার', 'মঙ্গলবার', 'বুধবার', 'বৃহস্পতিবার', 'শুক্রবার', 'শনিবার', 'রবিবার']
    if isinstance(date_input, str):
        date_obj = datetime.fromisoformat(date_input)
    elif isinstance(date_input, date):
        date_obj = date_input
    else:
        raise ValueError("Invalid date input")
    if lang == 'bn_ansi':
        return bangla_days_ansi[date_obj.weekday()]
    elif lang == 'bn_uni':
        return bangla_days_uni[date_obj.weekday()]
    else:
        raise ValueError("Invalid language code")

# Format date to string
def format_date(date_input, format_str='%d/%m/%Y'):
    if isinstance(date_input, str):
        date_obj = datetime.fromisoformat(date_input)
    elif isinstance(date_input, date):
        date_obj = date_input
    else:
        raise ValueError("Invalid date input")
    return date_obj.strftime(format_str)

@csrf_exempt
def generate_exam_resulation(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        academic_year = data.get('academic_year')
        exam_committee_id = data.get('exam_committee')
        get_semester = data.get('semester') # e.g., '1st Semester', '2nd Semester', etc.
        semester_dict = {str(choice[1]): choice[0] for choice in Course._meta.get_field('semester').choices} # {'1': '1st Semester', '2': '2nd Semester', ...}
        semester_ansi= '1g' if int(semester_dict.get(get_semester, 1)) % 2 == 1 else '2q'
        exam_type = data.get('exam_type')
        # Fetch the exam committee
        exam_committee = ExamCommittee.objects.filter(id=exam_committee_id).first()
        if not exam_committee:
            return JsonResponse({'error': 'Exam Committee not found'}, status=404)

        # Prepare context for the document
        committee_members = ExamCommitteeMember.objects.filter(committee=exam_committee)
        exam_commitee_chairman = committee_members.filter(role='chairman').first()
        external_member = committee_members.filter(role='external_member').first()
        external_member_dict_ansi={
            'name': external_member.teacher.full_name_ansi if external_member else 'N/A',
            'designation': external_member.teacher.get_designation_display(lang='bn_ansi') if external_member else 'N/A',
            'department': external_member.teacher.department.name_ansi if external_member else 'N/A',
            'university': external_member.teacher.university.name_ansi if external_member else 'N/A',
            'address': external_member.teacher.university.location_ansi if external_member else 'N/A',

         }
        
        courses=Course.objects.filter(syllabus__program=exam_committee.program)
        # construct context
        context = {
            'exam_committee_title': exam_committee.title_ansi,
            'exam_name_ansi': exam_committee.get_exam(exam_type).exam_name_ansi if exam_committee.get_exam(exam_type) else "No Exam",
            'start_date_of_exam': format_date(data.get('start_date_of_exam')) if data.get('start_date_of_exam') else '    /    /        ',
            'admission_session': exam_committee.get_addmission_session(),
            'semester': semester_ansi,
            'committee_members': committee_members,
            'committee_chairman': exam_commitee_chairman.teacher.full_name_ansi if exam_commitee_chairman else 'N/A',
            'external_member': external_member_dict_ansi if external_member else 'N/A',
            'academic_year': academic_year,
            'exam_type': exam_type,
            'courses': courses,
            'total_courses': courses.count(),
            'question_submission_deadline': format_date(data.get('question_submission_deadline')) if data.get('question_submission_deadline') else  '    /    /        ',
            'moderation_date': format_date(data.get('question_moderation_date_time')) if data.get('question_moderation_date_time') else 'N/A',
            'moderation_time': datetime.fromisoformat(data.get('question_moderation_date_time')).strftime('%I:%M') if data.get('question_moderation_date_time') else  '    /    /        ',
            'moderation_day' : get_bangla_day(data.get('question_moderation_date_time'), lang='bn_ansi') if data.get('question_moderation_date_time') else 'N/A',
            'viva_date_1': '10/11/2025',
            'viva_date_2': '11/11/2025',
            'duty_roster_made_by': data.get('duty_roster_made_by', 'N/A'),
            'resulation_date': format_date(data.get('resulation_date_time')) if data.get('resulation_date_time') else  '    /    /        ',
            'resulation_time': datetime.fromisoformat(data.get('resulation_date_time')).strftime('%I:%M') if data.get('resulation_date_time') else 'N/A',
            'resulation_day': get_bangla_day(data.get('resulation_date_time'), lang='bn_ansi') if data.get('resulation_date_time') else  '    /    /        ',
            'start_date_of_fillup': format_date(data.get('start_date_of_fillup')) if data.get('start_date_of_fillup') else 'N/A',
            'last_date_of_fillup': format_date(data.get('last_date_of_fillup')) if data.get('last_date_of_fillup') else 'N/A',
            'viva_dates': [format_date(date_str) for date_str in data.get('viva_dates', [])] or [],
        }
        # Load the template
        template_path = os.path.join(settings.BASE_DIR, 'templates/doc_file', 'Exam Resulation-1.docx')
        doc = DocxTemplate(template_path)
        # Render the template with the context
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
        'semesters': [choice[1] for choice in Course._meta.get_field('semester').choices],
        'teachers': Teacher.objects.all(),
    }
    return render(request, 'exams/Exam Resulation-1.html', web_context)
