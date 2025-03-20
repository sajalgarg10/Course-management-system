from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator 
from django.core.exceptions import ValidationError
from authentication.models import User , Base

# Create your models here.



class Course(Base):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    credits = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    passing_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )


class TeachersCoursesMapping(Base):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_teacher"
    )
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("course", "teacher")


    def save(self ,**kwargs):
        if self.teacher.role != "teacher" :
            raise ValidationError("Role should be teacher") 
        super().save( **kwargs)
        



