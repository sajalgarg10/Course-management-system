from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, TeachersCoursesMapping, CourseStudentMapping , GradeBook 
# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "role") 

@admin.register(Course)
class CustomCourseAdmin(admin.ModelAdmin):
    list_display = ("name", "credits") 

@admin.register(TeachersCoursesMapping)
class CustomTeacherCaoursesMappingAdmin(admin.ModelAdmin):
    list_display = ("get_teacher_username", "get_course_name" , "capacity") 

    def get_teacher_username(self, obj):
        return obj.teacher.username
    
    def get_course_name(self, obj):
        return obj.course.name
    
#admin.site.register(CourseStudentMapping)
@admin.register(CourseStudentMapping)
class CourseStudentMappingAdmin(admin.ModelAdmin):
    list_display = ("get_student_username" , "get_course_name", "status" ) 

    def get_student_username(self, obj):
        return obj.student.username
    
    def get_course_name(self, obj):
        return obj.course.name

@admin.register(GradeBook)
class GradeBookAdmin(admin.ModelAdmin):
    list_display = ("get_student_username", "get_course_name" , "marks_obtained" , "passing_marks" , "status"  ) 

    def get_student_username(self, obj):
        return obj.student.username
    
    def get_course_name(self, obj):
        return obj.course.name
    



