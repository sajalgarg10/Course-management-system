from django.db import models
from authentication.models import User , Base
from course.models import Course , TeachersCoursesMapping
from django.core.exceptions import ValidationError
# Create your models here.

class CourseStudentMapping(Base):
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT , related_name="course_student"
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
    status = models.CharField(
        max_length=9,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
        ],
        default="pending",
    )
    
    teacher= models.ForeignKey(
        User, on_delete=models.PROTECT , related_name="teacher"
    )

    class Meta:
        unique_together = (
            "course",
            "teacher",
            "student",
        )

    def save(self, **kwargs):
        obj = CourseStudentMapping.objects.active().filter(pk=self.pk).first()
        if obj and obj.status == "completed":
            raise ValidationError(" Cannot change for Completed status")
        if self.student.role != "student":
            raise ValidationError("Role should be student")
        if self.teacher.role != "teacher":
            raise ValidationError("Role should be teacher")
        teacher_course_mapping = TeachersCoursesMapping.objects.active().filter(teacher = self.teacher.pk , course = self.course.pk  )
        if not teacher_course_mapping:
            raise ValidationError("Teacher course mapping does not exists")
        super().save(**kwargs)
