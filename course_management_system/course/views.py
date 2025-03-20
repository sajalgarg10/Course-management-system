from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from helper.permissions import IsAdmin
from rest_framework import status
from rest_framework.response import Response
from .serializer import (
    CourseSerializer )
from .models import (
    Course
)
from django.core.exceptions import ObjectDoesNotExist 
from dashboard.models import CourseStudentMapping
from rest_framework import serializers

# Create your views here.


class CourseView(APIView):
    """
    Course API to post , update and delete course object
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    class ValidateInputDataCourseSerialier(serializers.Serializer):
        name = serializers.CharField(required = True)
        description = serializers.CharField(required=True)
        credits = serializers.IntegerField(required=True)
        passing_marks = serializers.FloatField(
            required=True, min_value=0.0, max_value=100.0
        )

    def post(self, request):
        validate_input_course_data = self.ValidateInputDataCourseSerialier(data=request.data)
        if not validate_input_course_data.is_valid():
            return Response({"message" :validate_input_course_data.errors }, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_input_course_data.save()
        except Exception as ex:
            return Response({"message": str(ex)}, status.HTTP_500_INTERNAL_SERVER_ERROR)  
        return Response(validate_input_course_data.data, status.HTTP_200_OK)
        

    def put(self, request, pk):
        course = Course.objects.active().filter(id = pk).first()   
        if not course:
            return Response({"message": "Couse does not exists"} , status=status.HTTP_404_NOT_FOUND ) 
        serializer_update_course = CourseSerializer(
            instance=course, data=request.data
        )
        if not serializer_update_course.is_valid():
            return Response({"message": serializer_update_course.errors} , status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer_update_course.save()
        except Exception as ex:
            return Response( {"meassage": str(ex)}, status.HTTP_500_INTERNAL_SERVER_ERROR)    
        return Response(serializer_update_course.data, status.HTTP_200_OK)
        
        
    def delete(self, request, pk):
        course_student_mapping =  CourseStudentMapping.objects.active().filter(course = pk)
        if course_student_mapping:
            return Response({"message": "Course can not be deleted"}, status.HTTP_400_BAD_REQUEST )
        try:
            course = Course.objects.get(id = pk)
            course.soft_delete()
        except ObjectDoesNotExist as ex:
                return Response( {"message": str(ex)}, status.HTTP_404_NOT_FOUND)     
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        return Response({"message": "Successfully deleted"}, status.HTTP_200_OK)
        
