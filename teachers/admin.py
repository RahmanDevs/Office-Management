from django.contrib import admin
from teachers.models import Teacher, University, Department, OfficeStaff
# Register your models here.
# admin.py
from django import forms
from django.contrib import admin





class TeacherAdmin(admin.ModelAdmin):
    # form = TeacherAdminForm
    list_display = ('full_name_en', 'full_name_uni', 'full_name_ar',  'email', 'phone_number', 'is_internal')
    search_fields = ('full_name_uni', 'full_name_ansi', 'full_name_en', 'full_name_ar', 'email')
    list_filter = ( 'is_internal',)
    ordering = ('-joining_date', )
    





    class Media:
        css = {
            'all': ('admin/css/sutonny_admin.css',)
        }

admin.site.register(Teacher, TeacherAdmin)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'short_name_en', 'location_en', 'website')
    search_fields = ('name_en', 'name_uni', 'short_name_en', 'location_en')
    list_filter = ('location_en',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'short_name_en', 'university', 'established_year', 'website')
    search_fields = ('name_en', 'name_uni', 'short_name_en', )
    list_filter = ('university',)


@admin.register(OfficeStaff)
class OfficeStaffAdmin(admin.ModelAdmin):
    list_display = ('full_name_en', 'full_name_uni', 'full_name_ar', 'designation', 'email', 'phone_number')
    search_fields = ('full_name_uni', 'full_name_ansi', 'full_name_en', 'full_name_ar', 'designation', 'email')
    list_filter = ('designation',)
    ordering = ('joining_date',)
    class Media:
        css = {
            'all': ('admin/css/sutonny_admin.css',)
        }
