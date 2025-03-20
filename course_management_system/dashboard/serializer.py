from rest_framework import serializers
from course.serializer import CourseSerializer
from .models import CourseStudentMapping


class CourseStudentMappingSerializer(serializers.ModelSerializer):
    course = CourseSerializer()    

    class Meta:
        model = CourseStudentMapping
        fields = ['id', 'course', 'status'  ]