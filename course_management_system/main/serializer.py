from rest_framework import serializers
from .models import User , Course , TeachersCoursesMapping , CourseStudentMapping , GradeBook

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' ,'role']

class RegisrationSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["password"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name' , 'description',  'credits' ]


class TeachersCoursesMappingSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  
    teacher = UserSerializer()  

    class Meta:
        model = TeachersCoursesMapping
        fields = ['id', 'course', 'teacher'  ]

class CourseStudentMappingSerializer(serializers.ModelSerializer):
    course = CourseSerializer()    

    class Meta:
        model = CourseStudentMapping
        fields = ['id', 'course', 'status'  ]

class GradeBookSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  
    student = UserSerializer()  

    class Meta:
        model =  GradeBook
        fields = ['id', 'course', 'student' , 'status' ,'marks_obtained' ,'passing_marks' ]        

