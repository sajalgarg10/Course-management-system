from rest_framework import serializers
from .models import GradeBook
from authentication.serializer import UserSerializer
from course.serializer import CourseSerializer



class GradeBookSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  
    student = UserSerializer()  

    class Meta:
        model =  GradeBook
        fields = ['id', 'course', 'student' , 'status' ,'marks_obtained'  ] 