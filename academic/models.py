from django.db import models
from teachers.models import Teacher, ExternalTeacher  # or Teacher if you named it that



SESSION_CHOICES = [
    ("2018-2019", "2018-2019"),
    ("2019-2020", "2019-2020"),
    ("2020-2021", "2020-2021"),
    ("2021-2022", "2021-2022"),
    ("2022-2023", "2022-2023"),
    ("2023-2024", "2023-2024"),
    ("2024-2025", "2024-2025"),
]

LEVEL_CHOICES = [
    ("1st Year", "1st Year"),
    ("2nd Year", "2nd Year"),
    ("3rd Year", "3rd Year"),
    ("4th Year", "4th Year"),
    ("Masters", "Masters"),
    ("MPhil", "MPhil"),
    ("PhD", "PhD"),
    ("EMTIS 1 year", "EMTIS 1 year"),
    ("EMTIS 2 year", "EMTIS 2 year"),
]

COMMITTEE_ROLE_CHOICES = [
    ("chairman", "Chairman"),
    ("member", "Member"),
    ("external_member", "External Member"),
    ("coordinator", "Coordinator"),
]

class AcademicYear(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    def __str__(self):
        return self.year

class Program(models.Model):
    title_en = models.CharField(max_length=255, blank=True, null=True)
    title_arabic = models.CharField(max_length=255, blank=True, null=True)
    title_uni = models.CharField(max_length=255, blank=True, null=True)
    title_ansi = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    admission_session = models.CharField(max_length=20, choices=SESSION_CHOICES)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='programs', blank=True, null=True)

    def __str__(self):
        return f"{self.title_en}:{self.level}-{self.academic_year}"
class Syllabus(models.Model):
    title=models.CharField(max_length=255, blank=True, null=True)
    program=models.ForeignKey(Program, on_delete=models.CASCADE, related_name='syllabus', blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}:{self.program}"


class Course(models.Model):
    SEMESTER_CHOICES = [
        ("1st Semester", "1st Semester"),
        ("2nd Semester", "2nd Semester"),
        ("3rd Semester", "3rd Semester"),
        ("4th Semester", "4th Semester"),
        ("5th Semester", "5th Semester"),
        ("6th Semester", "6th Semester"),
        ("7th Semester", "7th Semester"),
        ("8th Semester", "8th Semester"),
        ]

    course_code = models.CharField(max_length=50)
    title_en = models.CharField(max_length=255, blank=True, null=True)
    title_arabic = models.CharField(max_length=255, blank=True, null=True)
    title_uni = models.CharField(max_length=255, blank=True, null=True)
    title_ansi = models.CharField(max_length=255, blank=True, null=True)
    examin_1=models.ForeignKey(Teacher,related_name='courses_as_examiner1', on_delete=models.CASCADE,blank=True,null=True)
    examin_2=models.ForeignKey(Teacher,related_name='courses_as_examiner2', on_delete=models.CASCADE,blank=True,null=True)
    examin_3=models.ForeignKey(Teacher,related_name='courses_as_examiner3', on_delete=models.CASCADE,blank=True,null=True)
    examin_4=models.ForeignKey(Teacher,related_name='courses_as_examiner4', on_delete=models.CASCADE,blank=True,null=True)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, blank=True, null=True)
    course_credits = models.IntegerField(default=3)
    exam_hours = models.IntegerField(default=4)
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name='courses', blank=True, null=True)



    def __str__(self):
        return self.course_code

class ExamCommittee(models.Model):
    title_en = models.CharField(max_length=255, blank=True, null=True)
    title_uni = models.CharField(max_length=255, blank=True, null=True)
    title_ansi = models.CharField(max_length=255, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='exam_committee', blank=True, null=True)
    chairman = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='chairman_committees', blank=True, null=True)
    member=models.ManyToManyField(Teacher, related_name='member_committees',blank=True)
    external_member=models.ForeignKey(ExternalTeacher, on_delete=models.CASCADE, related_name='external_committees', blank=True, null=True)


    def __str__(self):
        return f"{self.title_uni}"


EXAM_TIME_CHOICES = [
    ("morning", "Morning"),
    ("afternoon", "Afternoon"),
]
class Exam(models.Model):
    # course_code = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exam', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.CharField(max_length=20, choices=EXAM_TIME_CHOICES)
    chief_inspector = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='chief_inspector', blank=True, null=True)
    inspectors = models.ManyToManyField(Teacher, related_name='inspectors', blank=True)
    # assistants = models.ManyToManyField(Employee)
    exam_committee = models.ForeignKey(ExamCommittee, on_delete=models.CASCADE, related_name='exam_committee', blank=True, null=True)

    def __str__(self):
        return f"{self.course.course_code if self.course else "No Course Code"}:{self.course} - {self.date} - {self.time}"
    def get_course_code(self):
        return self.course.course_code if self.course else "No Course Code"