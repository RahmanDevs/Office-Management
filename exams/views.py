from django.shortcuts import render
from academic.models import ExamCommittee
# from academic.models import ExamCommittee
# # Create your views here.

def create_exam_routine(request):
    

    context = {
        'committee_head': ExamCommittee.objects.all(),
    }
    return render(request, 'exams/exam_routine.html', context)

# make exam routine 
def exam_routine(request):
    return render(request, 'exams/exam_routine.html')


# from django.shortcuts import render

from django.http import HttpResponse
from django.conf import settings
from docxtpl import DocxTemplate
from teachers.models import Teacher, Officers
import os
import uuid
from datetime import date
from django.http import HttpResponse
from datetime import datetime


# # Create your views here.


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


def generate_duty_roster_docx(request):
    if request.method == "POST":
        # Read basic form fields
        program = request.POST.get("program")
        semester = request.POST.get("semester")
        chair_exam_committee = Teacher.objects.get(id=request.POST.get("chair_exam_committee"))
        exam_year=  request.POST.get("exam_year")
        exam_type = request.POST.get("exam_type")

        # Grouped course data
        course_rows = []
        total_rows = len(request.POST.getlist("course_code"))

        for i in range(total_rows):
            head_examiner=Teacher.objects.get(id=request.POST.getlist("head_examiner")[i])
            _envisilators=[]
            for inv in request.POST.getlist("envisilators")[i::total_rows]:
                inv_teacher=Teacher.objects.get(id=inv)
                _envisilators.append(inv_teacher.full_name_ansi)
            
            _assistants=[]
            for assis in request.POST.getlist("assistants")[i::total_rows]:
                assistants_obj=Officers.objects.get(id=assis)
                _assistants.append(assistants_obj.full_name_ansi)
            exam_date_obj = datetime.strptime(request.POST.getlist("exam_date")[i], "%Y-%m-%d")
            formatted_date = exam_date_obj.strftime("%d/%m/%Y")
            bangla_days = ['†mvgevi', 'g½jevi', 'eyaevi', 'e„n¯úwZevi', 'ïµevi', 'kwbevi', 'iweevi']
            bangla_day = bangla_days[exam_date_obj.weekday()]
            row = {
                "course_code": request.POST.getlist("course_code")[i],
                "exam_date": formatted_date,
                "exam_day": bangla_day,
                "exam_session": request.POST.getlist("exam_session")[i],
                "head_examiner":head_examiner.full_name_ansi,
                "envisilators": _envisilators,
                "assistants": _assistants,
            }
            course_rows.append(row)

        template_path = os.path.join(settings.BASE_DIR, 'templates\doc_file', 'Duty Roster.docx')
        doc = DocxTemplate(template_path)

        # Define context (dynamic data)
        context = {
            'program': program,
            'semester': semester,
            'course_rows':course_rows,
            'chair_exam_committee':chair_exam_committee.full_name_ansi,
            'exam_year':exam_year,
            'exam_type': exam_type
        }

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
    else:
        print('Get Request')
        get_context={
            'teachers':Teacher.objects.all(),
            'officers': Officers.objects.all()
        }
        return render(request, 'exams/duty_roster.html', context=get_context)


