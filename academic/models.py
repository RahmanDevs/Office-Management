from django.db import models
from teachers.models import Teacher, ExternalTeacher  # or Teacher if you named it that


class DepartmentDetails(models.Model):
    department_name_en = models.CharField(max_length=100)
    department_name_ansi = models.CharField(max_length=100)
    department_name_uni = models.CharField(max_length=100)

    current_department_head = models.OneToOneField(
        Teacher, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="headed_department"
    )

    def __str__(self):
        return self.department_name_en

SESSION_CHOICES = [
    ("2018-2019", "2018-2019"),
    ("2019-2020", "2019-2020"),
    ("2020-2021", "2020-2021"),
    ("2021-2022", "2021-2022"),
    ("2022-2023", "2022-2023"),
    ("2023-2024", "2023-2024"),
    ("2024-2025", "2024-2025"),
]
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

LEVEL_CHOICES = [
    ("Bachelor", "Bachelor"),
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
        return self.title

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
    course_code = models.CharField(max_length=50)
    title_en = models.CharField(max_length=255, blank=True, null=True)
    title_arabic = models.CharField(max_length=255, blank=True, null=True)
    title_uni = models.CharField(max_length=255, blank=True, null=True)
    title_ansi = models.CharField(max_length=255, blank=True, null=True)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, blank=True, null=True)
    course_credits = models.IntegerField(default=3)
    exam_hours = models.IntegerField(default=4)
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name='courses', blank=True, null=True)



    def __str__(self):
        return self.course_code

class CourseExaminer(models.Model):
    EXAMINER_TYPE=[
        ("Fist Examiner","Fist Examiner"),
        ("Second Examiner","Second Examiner"),
        ("Third Examiner","Third Examiner"),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='examiners')
    examiner = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course_examinations')
    examiner_type = models.CharField(max_length=50, choices=EXAMINER_TYPE, default="primary")
   

    def __str__(self):
        return f"{self.examiner} - {self.course}"

class ExamCommittee(models.Model):
    title_en = models.CharField(max_length=255, blank=True, null=True)
    title_uni = models.CharField(max_length=255, blank=True, null=True)
    title_ansi = models.CharField(max_length=255, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='exam_committee', blank=True, null=True)


    def __str__(self):
        return f"{self.title_uni}"
class ExamCommitteeMember(models.Model):

    COMMITTEE_ROLE_CHOICES = [
        ("chairman", "Chairman"),
        ("member", "Member"),
        ("external_member", "External Member"),
        ("coordinator", "Coordinator"),
    ]
    committee = models.ForeignKey(ExamCommittee, on_delete=models.CASCADE, related_name='members')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='committee_memberships')
    role = models.CharField(max_length=20, choices=COMMITTEE_ROLE_CHOICES)
    rank = models.PositiveSmallIntegerField(
        help_text="Lower number = higher priority"
    )

    def __str__(self):
        return f"{self.teacher} - {self.role} in {self.committee}"


class Exam(models.Model):
    EXAM_TIME_CHOICES = [
        ("morning", "Morning"),
        ("afternoon", "Afternoon"),
    ]
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