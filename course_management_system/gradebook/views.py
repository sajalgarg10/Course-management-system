from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStudent, IsTeacher
from rest_framework import status
from rest_framework.response import Response
from .serializer import (
    GradeBookSerializer )
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import (
    GradeBook
)
from dashboard.models import CourseStudentMapping
from rest_framework import serializers



class UpdateGradeBook(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    class ValidateInputDataGradeBookSerialier(serializers.Serializer):
        student_id = serializers.IntegerField(required=True)
        course_id = serializers.IntegerField(required=True)
        marks_obtained = serializers.FloatField(
            required=True, min_value=0.0, max_value=100.0
        )

    def post(self, request):
        id = request.user.id
        validate_input_data = self.ValidateInputDataGradeBookSerialier(
            data=request.data
        )
        if not (validate_input_data.is_valid()):
            return Response({"message": validate_input_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        student_id = validate_input_data.validated_data.get("student_id")
        course_id = validate_input_data.validated_data.get("course_id")
        course_student_queryset = CourseStudentMapping.objects.active().select_related(
            "teacher" , "student", "course"
        ).filter(teacher__id=id, course=course_id, student=student_id)
        if not course_student_queryset:
            return Response({"message": "Student course alloaction not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        for course_student_obj in course_student_queryset:
            grade_book = GradeBook(
                course=course_student_obj.course,
                marks_obtained=validate_input_data.validated_data.get(
                    "marks_obtained"
                ),
                student=course_student_obj.student,
            )
            try:
                with transaction.atomic():
                    grade_book.save()
                    course_student_obj.status = "completed"
                    course_student_obj.save()
            except ValidationError as ex:
                return Response({"message": ex.message}, status=status.HTTP_400_BAD_REQUEST)   
        return Response(
            {"meassage": "Successfully added grade"}, status.HTTP_200_OK
        )


class GetGradeBook(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        id = request.user.id
        grade_book = GradeBook.objects.active().select_related("course", "student").filter(
            student=id
        )
        serializer = GradeBookSerializer(grade_book, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
        

