from django.db import models

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


class Teacher(models.Model):
    
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
    ]
    full_name_uni = models.CharField(max_length=50)
    full_name_ansi = models.CharField(max_length=50)
    full_name_en = models.CharField(max_length=50, blank=True, null=True)
    full_name_ar = models.CharField(max_length=50, blank=True, null=True)
    short_name_en= models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    office_phone_number = models.CharField(max_length=15, blank=True, null=True)
    home_phone_number = models.CharField(max_length=15, blank=True, null=True)
    bank_account_number = models.CharField(max_length=30, blank=True, null=True)
    tin_number = models.CharField(max_length=30, blank=True, null=True)
    data_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    joining_date = models.DateField(blank=True, null=True)  
    def __str__(self):
        return f"{self.full_name_uni}"
    class Meta:
        ordering = ['joining_date']
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'



class ExternalTeacher(models.Model):
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
    ]
    full_name_uni = models.CharField(max_length=50)
    full_name_ansi = models.CharField(max_length=50)
    full_name_en = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # university= models.ForeignKey(University, on_delete=models.CASCADE, related_name='external_teachers', blank=True, null=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.full_name_en}"
    class Meta:
        verbose_name = 'External Teacher'
        verbose_name_plural = 'External Teachers'




class Officers(models.Model):
    DESIGNATION_CHOICES = [
        ('assistant_registrar', 'Assistant Registrar'),
        ('section_officer', 'Section Officer'),
        ('computer_oparator', 'Computer Oparator'),
        ('office_assistant', 'Office Assistant'),
    ]
    full_name_uni = models.CharField(max_length=50)
    full_name_ansi = models.CharField(max_length=50)
    full_name_en = models.CharField(max_length=50, blank=True, null=True)
    full_name_ar = models.CharField(max_length=50, blank=True, null=True)
    short_name_en= models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    office_phone_number = models.CharField(max_length=15, blank=True, null=True)
    home_phone_number = models.CharField(max_length=15, blank=True, null=True)
    bank_account_number = models.CharField(max_length=30, blank=True, null=True)
    tin_number = models.CharField(max_length=30, blank=True, null=True)
    data_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    joining_date = models.DateField(blank=True, null=True)  
    def __str__(self):
        return f"{self.full_name_uni}"
    class Meta:
        ordering = ['joining_date']
        verbose_name = 'Officer'
        verbose_name_plural = 'Officers'
