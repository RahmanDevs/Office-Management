from django.contrib import admin
from academic import forms
import nested_admin
# import InlineModelAdmin
from django.contrib.admin import TabularInline
from .models import (
    ExamCommittee, 
    Program, Syllabus,
    Course,
    AcademicYear,
    ExamRutine,
    Exam,
    DepartmentDetails, ExamCommitteeMember, CourseExaminer
)
from django.utils.html import format_html

class ExamRutineInline(admin.TabularInline):
    model = ExamRutine
    extra = 1
    

class ExaminerInline(nested_admin.NestedTabularInline):
    model = CourseExaminer
    extra = 1

class CourseInline(nested_admin.NestedStackedInline):

    model = Course
    inlines = [ExaminerInline]
    extra = 1
    # add ExamRutine inline
    inlines = [ExamRutineInline]

@admin.register(Syllabus)
class SyllabusAdmin(nested_admin.NestedModelAdmin):
    inlines = [CourseInline]




@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'code', 'level', 'admission_session', 'academic_year')
    search_fields = ('title_en', 'title_arabic', 'title_uni', 'title_ansi', 'code')
    list_filter = ('level', 'admission_session', 'academic_year')
    class Media:
        css = {
            'all': ('admin/css/sutonny_admin.css',)
        }

class DepartmentDetailsAdmin(admin.ModelAdmin):
    list_display = ('department_name_en', 'current_department_head')
    search_fields = ('department_name_en', 'current_department_head')
admin.site.register(DepartmentDetails, DepartmentDetailsAdmin)

class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'year')
    search_fields = ('title', 'year')
    list_filter = ('start_date', 'end_date')

admin.site.register(AcademicYear, AcademicYearAdmin)

# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('course_code', 'title_en', 'title_arabic', 'title_uni', )
#     search_fields = ('course_code',)
#     list_filter = ('syllabus',)
#     # add Course Examining Teachers in tabular form
#     inlines = [CourseExaminerAdmin]

#     def syllabus(self, obj):
#         return obj.syllabus.title if obj.syllabus else "No Syllabus"

# admin.site.register(Course, CourseAdmin)
admin.site.register(Exam)

class ExamAdmin(admin.TabularInline):
    model = Exam
    extra = 1



class ExamCommitteeMemberAdmin(TabularInline):
    model = ExamCommitteeMember
    extra = 1
@admin.register(ExamCommittee)
class CommitteeAdmin(admin.ModelAdmin):
    inlines = [ExamCommitteeMemberAdmin, ExamAdmin]
    list_display = ('title_uni',  'session', 'year', 'level')
    search_fields = ('title_uni', )
    def program(self, obj):
        return obj.program.title_en if obj.program else "No Program"
    def session(self, obj):
        return obj.program.admission_session if obj.program else "No Session"
    def year(self, obj):
        return obj.program.academic_year.year if obj.program and obj.program.academic_year else "No Year"
    def level(self, obj):
        return obj.program.level if obj.program else "No Level"
    

# admin.site.register(Exam)
# Define the role priority
# class ExamCommitteeAdmin(admin.ModelAdmin):
#     list_display = ('title_uni', 'program',  'member_list',)
#     search_fields = ('title_uni', )


#     def member_list(self, obj):
#         members = ExamCommitteeMember.objects.filter(committee=obj)
#         return format_html(", ".join([str(member) for member in members])) if members else "No Members"
#     def program(self, obj):
#         return obj.program.name_uni if obj.program else "No Program"
#     def session(self, obj):
#         return obj.program.session if obj.program else "No Session"
#     def year(self, obj):
#         return obj.program.year if obj.program else "No Year"
#     def level(self, obj):
#         return obj.program.level if obj.program else "No Level"
    




# class ExamAdmin(admin.ModelAdmin):
#     list_display = ('course_code', 'date', 'time', 'chief_inspector', 'inspectors_list', 'examin','exam_committee')
#     search_fields = ('course_code', 'date')
#     list_filter = ('date', 'time')
#     def examin(self, obj):
#         return format_html("<br>".join([str(obj.course.examin_1), str(obj.course.examin_2), str(obj.course.examin_3), str(obj.course.examin_4)])) if obj else "No Examiners"
#     def inspectors_list(self, obj):
#         inspectors = obj.inspectors.all()
#         return format_html("<br>".join([str(inspector) for inspector in inspectors])) if inspectors else "No Inspectors"
#     def course_code(self, obj):
#         return obj.course.course_code if obj.course else "No Course Code"
#     inspectors_list.short_description = "Inspectors"


# admin.site.register(Exam, ExamAdmin)


# admin.site.register(Program, ProgramAdmin)

# admin.site.register(ExamCommittee, ExamCommitteeAdmin)

