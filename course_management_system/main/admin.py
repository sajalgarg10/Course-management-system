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

admin.site.register(TeachersCoursesMapping)
admin.site.register(CourseStudentMapping)
admin.site.register(GradeBook)

