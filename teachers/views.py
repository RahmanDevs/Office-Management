from django.views.generic import ListView
from teachers.models import Teacher, University, Department  # Import your Teacher model here



class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'  # Replace with your actual template name
    context_object_name = 'teachers'  # The name of the variable to be used in the template

class FacultyListView(ListView):
    model = Teacher
    template_name = 'teachers/faculty_member_list.html'  # Replace with your actual template name
    context_object_name = 'faculties'  # The name of the variable to be used in the template

    department_obj=Department.objects.filter(name_en='Department of Al-Quran & Islamic Studies').first()
    university_obj=University.objects.filter(name_en='Islamic University').first()

    def get_queryset(self):
        return Teacher.objects.filter(department=self.department_obj, university=self.university_obj)  # Adjust the filter as needed for faculty members