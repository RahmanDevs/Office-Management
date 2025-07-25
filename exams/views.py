import os
from django.shortcuts import render
from academic.models import ExamCommittee
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from docxtpl import DocxTemplate
from teachers.models import Teacher, Officers
import uuid
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt
import json




def create_exam_routine(request):
    

    context = {
        'committee_head': ExamCommittee.objects.all(),
    }
    return render(request, 'exams/exam_routine.html', context)

# make exam routine 
def exam_routine(request):
    return render(request, 'exams/exam_routine.html')


# from django.shortcuts import render


# # Create your views here.

def generate_moderation_letter(request):
    return HttpResponse(f"""
<ol>

""")

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

@csrf_exempt  
def generate_duty_roster_docx(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Basic fields
            program = data.get("program")
            semester = data.get("semester")
            exam_year = data.get("exam_year")
            exam_type = data.get("exam_type")
            chair_exam_committee = Teacher.objects.get(id=data.get("chair_exam_committee"))
            courses=data.get("courses", [])
            course_rows = []
            for row in courses:
                exam_date_obj = datetime.strptime(row["exam_date"], "%Y-%m-%d")
                formatted_date = exam_date_obj.strftime("%d/%m/%Y")
                bangla_days = ['†mvgevi', 'g½jevi', 'eyaevi', 'e„n¯úwZevi', 'ïµevi', 'kwbevi', 'iweevi']
                bangla_day = bangla_days[exam_date_obj.weekday()]
                course_rows.append({
                    "course_code": row['course_code'],
                    "exam_date": formatted_date,
                    "exam_day": bangla_day,
                    "exam_session": row['exam_session'],
                    "head_examiner": row['head_examiner'],
                    "envisilators": row['envisilators'] or [],
                    "assistants": row['assistants'] or [],
                })
            # Template and context
            template_path = os.path.join(settings.BASE_DIR, 'templates/doc_file', 'Duty Roster.docx')
            doc = DocxTemplate(template_path)
            context = {
                'program': program,
                'semester': semester,
                'course_rows': course_rows,
                'chair_exam_committee': chair_exam_committee.full_name_ansi,
                'exam_year': exam_year,
                'exam_type': exam_type
            }
            # Render and save the document
            doc.render(context)
            file_name = f"generated_{uuid.uuid4()}.docx"
            output_path = os.path.join(settings.MEDIA_ROOT, file_name)
            doc.save(output_path)
            # Return the file
            with open(output_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(),
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = f'attachment; filename={file_name}'
                return response
            # return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # For GET requests, render the page
        context = {
            'teachers': Teacher.objects.all(),
            'officers': Officers.objects.all()
        }
        return render(request, 'exams/duty_roster.html', context=context)
@csrf_exempt  
def generate_exam_bill_notesheet(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)

            # Basic fields
            program = data.get("program")
            semester = data.get("semester")
            exam_year = data.get("exam_year")
            exam_type = data.get("exam_type")
            amount = data.get("amount")
            num_of_teacher = data.get("num_of_teacher")

            chair_exam_committee = Teacher.objects.get(id=data.get("chair_exam_committee"))

            course_rows = []
            print("Course Rows Data: ", data.get("courses", []))
            courses=data.get("courses", [])
            for row in courses:
                # head_examiner = Teacher.objects.get(id=row.get("head_examiner"))

                # _envisilators = []
                # for inv_id in row.get("envisilators", []):
                #     inv_teacher = Teacher.objects.get(id=inv_id)
                #     _envisilators.append(inv_teacher.full_name_ansi)

                # _assistants = []
                # for assis_id in row.get("assistants", []):
                #     assistant = Officers.objects.get(id=assis_id)
                #     _assistants.append(assistant.full_name_ansi)

                exam_date_obj = datetime.strptime(row["exam_date"], "%Y-%m-%d")
                formatted_date = exam_date_obj.strftime("%d/%m/%Y")
                bangla_days = ['†mvgevi', 'g½jevi', 'eyaevi', 'e„n¯úwZevi', 'ïµevi', 'kwbevi', 'iweevi']
                bangla_day = bangla_days[exam_date_obj.weekday()]

                course_rows.append({
                    "course_code": row['course_code'],
                    "exam_date": formatted_date,
                    "exam_day": bangla_day,
                    "exam_session": row['exam_session'],
                    "head_examiner": row['head_examiner'],
                    # "envisilators": _envisilators,
                    "envisilators": row['envisilators'] or [],
                    "assistants": row['assistants'] or [],
                })
            # Template and context
            template_path = os.path.join(settings.BASE_DIR, 'templates/doc_file/exam', 'exam_bill_notesheet.docx')
            doc = DocxTemplate(template_path)
            context = {
                'program': program,
                'semester': semester,
                'chair_exam_committee': chair_exam_committee.full_name_ansi,
                'exam_year': exam_year,
                'exam_type': exam_type,
                'amount': amount,
                'num_of_teacher':num_of_teacher,
                'amount_word':'kjhjjhjhjshdf'
            }

            # Render and save the document
            doc.render(context)
            file_name = f"generated_{uuid.uuid4()}.docx"
            output_path = os.path.join(settings.MEDIA_ROOT, file_name)
            doc.save(output_path)

            # Return the file
            with open(output_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(),
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
                response['Content-Disposition'] = f'attachment; filename={file_name}'
                return response
            # return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # For GET requests, render the page
        context = {
            'teachers': Teacher.objects.all(),
            'officers': Officers.objects.all()
        }
        return render(request, 'exams/exam_bill_notesheet.html', context=context)





