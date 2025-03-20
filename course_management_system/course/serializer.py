from rest_framework import serializers
from .models import Course , TeachersCoursesMapping 
from authentication.serializer import UserSerializer



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name' , 'description',  'credits' , 'passing_marks' ]


class TeachersCoursesMappingSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  
    teacher = UserSerializer()  

    class Meta:
        model = TeachersCoursesMapping
        fields = ['id', 'course', 'teacher'  ]