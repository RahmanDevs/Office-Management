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
    # Order by admission session descending
    class Meta:
        ordering = ['-admission_session']
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
    def get_examiner(self, examiner_type="First Examiner"):
        """
        Example usage in docxtpl template:
        {{ course.get_examiner("First Examiner") }}
        {{ course.get_examiner("Second Examiner") }}
        """
        examiner = CourseExaminer.objects.get(course=self, examiner_type=examiner_type)
        if examiner:
            return examiner.examiner.full_name_ansi
        return "No First Examiner assigned"
    
    def get_exam_date(self):
        print("Getting exam date...")

        """
        Example usage in docxtpl template:
        {{ course.get_exam_date() }}
        {{ course.get_exam_date()[0] }} # gets date
        {{ course.get_exam_date()[1] }} # gets day in Bangla
        {{ course.get_exam_date()[2] }} # gets time
        {{ course.get_exam_date()[3] }} # gets room in Bangla


        """
        EXAM_TIME={
            "morning": "09:30-01:30",
            "afternoon": "01:30-05:30",
            }
        exam = Exam.objects.filter(course=self).first()
        exam_date=exam.date
        bangla_days = ['†mvgevi', 'g½jevi', 'eyaevi', 'e„n¯úwZevi', 'ïµevi', 'kwbevi', 'iweevi']
        bangla_day_ansi = bangla_days[exam_date.weekday()]
        exam_time=EXAM_TIME.get(exam.time)
        exam_room_ansi=exam.get_exam_room('bn_ansi')
        if not exam_time:
            exam_time="No Exam Time Assigned"
        if not exam_date:
            exam_date="No Exam Date Assigned"
        print(exam_room_ansi)
        print(exam_time)
        print(bangla_day_ansi)
        print(exam_date)
        return str(exam_date.strftime("%d/%m/%Y")), f"{bangla_day_ansi}", str(exam_time), str(exam_room_ansi)
        


class CourseExaminer(models.Model):
    EXAMINER_TYPE=[
        ("First Examiner","First Examiner"),
        ("Second Examiner","Second Examiner"),
        ("Third Examiner","Third Examiner"),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='examiners')
    examiner = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course_examinations')
    examiner_type = models.CharField(max_length=50, choices=EXAMINER_TYPE, default="primary")
   

    def __str__(self):
        return f"{self.examiner} - {self.course}"


class ExamRoom(models.TextChoices):
    ROOM_101 = ("Room 101", "Room 101")
    ROOM_102 = ("Room 102", "Room 102")
    ROOM_103 = ("Room 103", "Room 103")
    ROOM_104 = ("Room 104", "Room 104")

EXAM_ROOM_CHOICES={
        "Room 101":{
            'en': 'Faculty Bulting-201',
            'bn_uni': 'অনুষদ ভবন-201',
            'bn_ansi': 'Abyl` feb-201',
            'ar': 'الغرفة 101',
        },
        "Room 102":{
            'en': 'Faculty Building-202',
            'bn_uni': 'অনুষদ ভবন-202',
            'bn_ansi': 'Abyl` feb-202',
            'ar': 'الغرفة 102',
        },
        "Room 103":{
            'en': 'Faculty Building-203',
            'bn_uni': 'অনুষদ ভবন-203',
            'bn_ansi': 'Abyl` feb-203',
            'ar': 'الغرفة 103',
        },
        "Room 104":{
            'en': 'Faculty Building-204',
            'bn_uni': 'অনুষদ ভবন-204',
            'bn_ansi': 'Abyl` feb-204',
            'ar': 'الغرفة 104',
        },
    }

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
    room_number = models.CharField(choices=ExamRoom.choices, max_length=50, blank=True, null=True, default="Room 103")

    def __str__(self):
        return f"{self.course.course_code if self.course else "No Course Code"}:{self.course} - {self.date} - {self.time}"
    def get_exam_room(self, lang='en'):
        """
        Example usage in docxtpl template:
        {{ exam.get_exam_room('ar') }}
        """
        return EXAM_ROOM_CHOICES.get(self.room_number, {}).get(lang, self.room_number)

    def get_course_code(self):
        return self.course.course_code if self.course else "No Course Code"

class ExamCommittee(models.Model):
    title_en = models.CharField(max_length=255, blank=True, null=True)
    title_uni = models.CharField(max_length=255, blank=True, null=True)
    title_ansi = models.CharField(max_length=255, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='exam_committee', blank=True, null=True)


    def __str__(self):
        return f"{self.title_en} - {self.program}"


ROLE_LANG = {
    'chairman': {
        'en': 'Chairman',
        'bn_uni': 'সভাপতি',
        'bn_ansi': 'mfvcwZ',
        'ar': 'رئيس اللجنة',
    },
    'member': {
        'en': 'Member',
        'bn_uni': 'সদস্য',
        'bn_ansi': 'm`m¨',
        'ar': 'عضو',
    },
    'external_member': {
        'en': 'External Member',
        'bn_uni': 'বহিস্থ সদস্য',
        'bn_ansi': 'ewn¯’ m`m¨',
        'ar': 'عضو خارجي',
    },
    'coordinator': {
        'en': 'Coordinator',
        'bn_uni': 'কোর্ডিনেটর',
        'bn_ansi': '†KvAwW©‡bUi',
        'ar': 'منسق',
    },
}


class Role(models.TextChoices):
        CHAIRMAN = ('chairman', 'Chairman')
        MEMBER = ('member', 'Member')
        EXTERNAL_MEMBER = ('external_member', 'External Member')
        COORDINATOR = ('coordinator', 'Coordinator')


class ExamCommitteeMember(models.Model):

    committee = models.ForeignKey(ExamCommittee, on_delete=models.CASCADE, related_name='members')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='committee_memberships')
    role = models.CharField(max_length=20, choices=Role.choices)
    rank = models.PositiveSmallIntegerField(
        help_text="Lower number = higher priority"
    )

    def __str__(self):
        return f"{self.teacher} - {self.role} in {self.committee}"
    def get_role(self, lang='en'):
        """
        Example usage in docxtpl template:
        {{ member.get_role('ar') }}
        """
        return ROLE_LANG.get(self.role, {}).get(lang, self.role)



