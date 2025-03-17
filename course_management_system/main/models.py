from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.


class User(AbstractUser):
    role = models.CharField(
        max_length=9,
        choices=[("admin", "Admin"), ("student", "Student"), ("teacher", "Teacher")],
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    


class Course(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    credits = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TeachersCoursesMapping(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_teacher"
    )
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "teacher")


class CourseStudentMapping(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_student"
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
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # teacher mapping name change
    teacher= models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="teacher"
    )

    class Meta:
        unique_together = (
            "course",
            "teacher",
            "student",
        )

    # TODO RECHECK LOGIC
    def save(self, **kwargs):
        obj = CourseStudentMapping.objects.filter(pk=self.pk).first()
        if obj and obj.status == "Completed":
            raise ValueError(" Cannot change for Completed status")
        super().save(**kwargs)


# TODO RECHECK LOGIC COURSE FOREIGN
class GradeBook(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    passing_marks = models.DecimalField(
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
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # TODO RECHECK LOGIC
    def clean(self):
        super().clean()
        if self.marks_obtained < self.passing_marks:
            self.status = "Fail"
        else:
            self.status = "Pass"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
