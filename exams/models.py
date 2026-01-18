from django.db import models
from academic.models import Course
from teachers.models import Teacher, Officers

# Create your models here.

# Create Exam Duty Roster

# class DutyRoster(models.Model):
#     exam_head = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='exam_head')
#     invisilators = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='invisilators')
#     officers = models.ForeignKey(Officers, on_delete=models.CASCADE, related_name='officers')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.exam_head.full_name_en} - {self.course.title_en}"

#     class Meta:
#         verbose_name = "Exam Duty Roster"
#         verbose_name_plural = "Exam Duty Rosters"

