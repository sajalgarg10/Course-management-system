from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from authentication.models import User , Base
from course.models import Course
from dashboard.models import CourseStudentMapping

# Create your models here.

class GradeBook(Base):
    course = models.ForeignKey(Course, on_delete=models.PROTECT )
    marks_obtained = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    status = models.CharField(
        max_length=9,
        choices=[
            ("pass", "Pass"),
            ("fail", "Fail"),
        ],
        blank=True,
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if self.marks_obtained < self.course.passing_marks:
            self.status = "fail"
        else:
            self.status = "pass"

    def save(self, *args, **kwargs):
        self.clean()
        if self.student.role != "student":
            raise ValidationError("Role should be student")
        course_student_mapping = CourseStudentMapping.objects.active().filter(course = self.course.pk , student = self.student.pk )
        if not course_student_mapping:
            raise ValidationError("Student course mapping does not exist")


        super().save(*args, **kwargs)