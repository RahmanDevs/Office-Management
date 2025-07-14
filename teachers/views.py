from django.views.generic import ListView
from teachers.models import Teacher  # Import your Teacher model here



class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'  # Replace with your actual template name
    context_object_name = 'teachers'  # The name of the variable to be used in the template

class FacultyListView(ListView):
    model = Teacher
    template_name = 'teachers/faculty_member_list.html'  # Replace with your actual template name
    context_object_name = 'faculties'  # The name of the variable to be used in the template

    def get_queryset(self):
        return Teacher.objects.filter(designation='professor')  # Adjust the filter as needed for faculty members