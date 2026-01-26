from django.db import models
from django.forms import ValidationError

# Create your models here.

class University(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_ansi = models.CharField(max_length=255, unique=True)
    name_uni = models.CharField(max_length=255, unique=True)
    short_name_en = models.CharField(max_length=100, blank=True, null=True)  # e.g. "DU", "RU"
    short_name_ansi = models.CharField(max_length=100, blank=True, null=True)  # e.g. "DU", "RU"
    short_name_uni = models.CharField(max_length=100, blank=True, null=True)  # e.g. "DU", "RU"
    location_en = models.CharField(max_length=255, blank=True, null=True)
    location_ansi = models.CharField(max_length=255, blank=True, null=True)
    location_uni = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"


class Department(models.Model):
    name_en = models.CharField(max_length=255, blank=True, null=True)
    name_ansi = models.CharField(max_length=255, blank=True, null=True)
    name_uni = models.CharField(max_length=255, blank=True, null=True)
    short_name_en = models.CharField(max_length=100, blank=True, null=True)
    short_name_ansi = models.CharField(max_length=100, blank=True, null=True)
    short_name_uni = models.CharField(max_length=100, blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='departments')
    established_year = models.PositiveIntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name_en']

    def __str__(self):
        return f"{self.name_en} ({self.university.short_name_en})"

DESIGNATION_LANG={

    'Professor': {
        'title_bn_ansi': 'Aa¨vcK',
        'title_bn_uni': 'অধ্যাপক',
        'title_en': 'Professor',
        'title_ar': 'أستاذ',
    },
    'Associate Professor': {
        'title_bn_ansi': 'm‡nv‡hvMx Aa¨vcK',
        'title_bn_uni': 'সহযোগী অধ্যাপক',
        'title_en': 'Associate Professor',
        'title_ar': 'أستاذ مشارك',
    },
    'Assistant Professor': {
        'title_bn_ansi': 'mnKvix Aa¨vcK',
        'title_bn_uni': 'সহকারী অধ্যাপক',
        'title_en': 'Assistant Professor',
        'title_ar': 'مساعد أستاذ',
    },
    'Lecturer': {
        'title_bn_ansi': '†jKPvivi',
        'title_bn_uni': 'লেকচারার',
        'title_en': 'Lecturer',
        'title_ar': 'محاضر',
    },

}


class Designation(models.IntegerChoices):
    PROFESSOR = 1, "Professor"
    ASSOCIATE = 2, "Associate Professor"
    ASSISTANT = 3, "Assistant Professor"
    LECTURER = 4, "Lecturer"

class Teacher(models.Model):

    full_name_uni = models.CharField(max_length=50)
    full_name_ansi = models.CharField(max_length=50)
    full_name_en = models.CharField(max_length=50, blank=True, null=True)
    full_name_ar = models.CharField(max_length=50, blank=True, null=True)
    short_name_en= models.CharField(max_length=50, blank=True, null=True)
    university=models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    designation = models.PositiveSmallIntegerField(choices=Designation.choices, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    office_phone_number = models.CharField(max_length=15, blank=True, null=True)
    home_phone_number = models.CharField(max_length=15, blank=True, null=True)
    bank_account_number = models.CharField(max_length=30, blank=True, null=True)
    tin_number = models.CharField(max_length=30, blank=True, null=True)
    data_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/Teachers/', blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    is_internal= models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.full_name_en}"
    def get_designation_display(self, lang='en'):
        if self.designation:
            if lang == 'en':
                return Designation(self.designation).label
            elif lang == 'bn_ansi':
                return DESIGNATION_LANG.get(Designation(self.designation).label, {}).get('title_bn_ansi', 'N/A')
            elif lang == 'bn_uni':
                return DESIGNATION_LANG.get(Designation(self.designation).label, {}).get('title_bn_uni', 'N/A')
            elif lang == 'ar':
                return DESIGNATION_LANG.get(Designation(self.designation).label, {}).get('title_ar', 'N/A')
        return "N/A"
    def clean(self):
        if self.university and self.department:
            if self.university.name_en == 'Islamic University' and self.department.name_en == 'Department of Al-Quran & Islamic Studies':
                self.is_internal = True
            else:
                self.is_internal = False    


        if self.department and self.university:
            if self.department.university != self.university:
                raise ValidationError("Department does not belong to selected university.")
                
                        
    class Meta:
        ordering = ['joining_date','designation']
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

class OfficeStaff(models.Model):
    DESIGNATION_CHOICES = [
        (1, 'Assistant Registrar'),
        (2, 'Section Officer'),
        (3, 'Administrative officer'),
        (4, 'Computer Oparator'),
        (5, 'Office Assistant'),
    ]
    full_name_uni = models.CharField(max_length=50)
    full_name_ansi = models.CharField(max_length=50)
    full_name_en = models.CharField(max_length=50, blank=True, null=True)
    full_name_ar = models.CharField(max_length=50, blank=True, null=True)
    short_name_en= models.CharField(max_length=50, blank=True, null=True)
    university=models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    designation = models.PositiveSmallIntegerField(choices=DESIGNATION_CHOICES, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    office_phone_number = models.CharField(max_length=15, blank=True, null=True)
    home_phone_number = models.CharField(max_length=15, blank=True, null=True)
    bank_account_number = models.CharField(max_length=30, blank=True, null=True)
    tin_number = models.CharField(max_length=30, blank=True, null=True)
    data_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/OfficeStaff/', blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)  
    def __str__(self):
        return f"{self.full_name_en}"   
    def clean(self):
        if self.department and self.university:
            if self.department.university != self.university:
                raise ValidationError("Department does not belong to selected university.")
    class Meta:
        ordering = ['joining_date','designation']
        verbose_name = 'Office Staff'
        verbose_name_plural = 'Office Staffs'


