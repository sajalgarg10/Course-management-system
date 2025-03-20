from django.contrib import admin
from .models import GradeBook
# Register your models here.


@admin.register(GradeBook)
class CustomGradeBookAdmin(admin.ModelAdmin):
    list_display = ( "status" , "get_student_username" , "get_course_name" , "marks_obtained" ) 
    def get_student_username(self, obj):
        return obj.student.username  
    get_student_username.short_description = "Student"

    def get_course_name(self, obj):
        return obj.course.name  
    get_course_name.short_description = "Course" 
