from django.contrib import admin
from .models import Course, TeachersCoursesMapping

# Register your models here.


@admin.register(Course)
class CustomCourseAdmin(admin.ModelAdmin):
    list_display = ("name", "credits" , "passing_marks") 

admin.site.register(TeachersCoursesMapping)
