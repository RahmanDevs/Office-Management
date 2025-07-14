from django.contrib import admin
from .models import ExamCommittee, Exam, Program, Syllabus, Course
from django.utils.html import format_html


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'examin_1', 'examin_2', 'examin_3', 'examin_4', 'course_credits', 'exam_hours')
    search_fields = ('course_code', 'course_name')
    list_filter = ('syllabus',)

    def syllabus(self, obj):
        return obj.syllabus.title if obj.syllabus else "No Syllabus"

admin.site.register(Course, CourseAdmin)


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_arabic', 'name_uni', 'name_ansi', 'code', 'level', 'session', 'year')
    search_fields = ('name_en', 'name_arabic', 'name_uni', 'name_ansi', 'code')
    list_filter = ('level', 'session')

class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('title', 'program')



# Define the role priority
class ExamCommitteeAdmin(admin.ModelAdmin):
    list_display = ('title_uni', 'program', 'session', 'year', 'level', 'chairman', 'external_member', 'member_list',)
    search_fields = ('title_uni', 'session', 'year', 'level')
    # list_filter = ('session', 'year', 'level')

    def member_list(self, obj):
        members = obj.member.all()
        return format_html(", ".join([str(member) for member in members])) if members else "No Members"
    def program(self, obj):
        return obj.program.name_uni if obj.program else "No Program"
    def session(self, obj):
        return obj.program.session if obj.program else "No Session"
    def year(self, obj):
        return obj.program.year if obj.program else "No Year"
    def level(self, obj):
        return obj.program.level if obj.program else "No Level"
    
    member_list.short_description = "Members"



class ExamAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'date', 'time', 'chief_inspector', 'inspectors_list', 'examin','exam_committee')
    search_fields = ('course_code', 'date')
    list_filter = ('date', 'time')
    def examin(self, obj):
        return format_html("<br>".join([str(obj.course.examin_1), str(obj.course.examin_2), str(obj.course.examin_3), str(obj.course.examin_4)])) if obj else "No Examiners"
    def inspectors_list(self, obj):
        inspectors = obj.inspectors.all()
        return format_html("<br>".join([str(inspector) for inspector in inspectors])) if inspectors else "No Inspectors"
    def course_code(self, obj):
        return obj.course.course_code if obj.course else "No Course Code"
    inspectors_list.short_description = "Inspectors"


admin.site.register(Exam, ExamAdmin)

admin.site.register(Program, ProgramAdmin)
admin.site.register(Syllabus, SyllabusAdmin)
admin.site.register(ExamCommittee, ExamCommitteeAdmin)