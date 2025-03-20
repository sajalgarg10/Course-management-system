from django.contrib import admin
from .models import CourseStudentMapping

@admin.register(CourseStudentMapping)
class CustomCourseStudentAdmin(admin.ModelAdmin):
    list_display = ( "status" , "get_student_username" , "get_course_name" ,  "get_teacher_username" ) 
    def get_student_username(self, obj):
        return obj.student.username  
    get_student_username.short_description = "Student"

    def get_course_name(self, obj):
        return obj.course.name  
    get_course_name.short_description = "Course" 

    def get_teacher_username(self, obj):
        return obj.teacher.username  
    get_teacher_username.short_description = "Teacher"


# Register your models here.
