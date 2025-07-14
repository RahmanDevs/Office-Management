from django.contrib import admin
from teachers.models import Teacher,ExternalTeacher, University, Department, Officers
# Register your models here.

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name_en', 'full_name_uni', 'full_name_ar', 'designation', 'email', 'phone_number')
    search_fields = ('full_name_uni', 'full_name_ansi', 'full_name_en', 'full_name_ar', 'designation', 'email')
    list_filter = ('designation',)
    ordering = ('joining_date',)

admin.site.register(Teacher, TeacherAdmin)
class ExternalTeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name_en', 'full_name_uni',  'designation', 'email', 'phone_number')
    search_fields = ('full_name_uni', 'full_name_ansi', 'full_name_en', 'phone_number', 'designation', 'email')
    list_filter = ('designation',)


admin.site.register(ExternalTeacher, ExternalTeacherAdmin)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'short_name_en', 'location_en', 'website')
    search_fields = ('name_en', 'name_uni', 'short_name_en', 'location_en')
    list_filter = ('location_en',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'short_name_en', 'university', 'established_year', 'website')
    search_fields = ('name_en', 'name_uni', 'short_name_en')
    list_filter = ('university',)


@admin.register(Officers)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ('full_name_en', 'full_name_uni', 'full_name_ar', 'designation', 'email', 'phone_number')
    search_fields = ('full_name_uni', 'full_name_ansi', 'full_name_en', 'full_name_ar', 'designation', 'email')
    list_filter = ('designation',)
    ordering = ('joining_date',)
