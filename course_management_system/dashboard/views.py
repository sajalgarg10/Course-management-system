from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStudent, IsTeacher
from rest_framework import status
from authentication.serializer import UserSerializer
from rest_framework.response import Response
from .serializer import (
    CourseStudentMappingSerializer,
)
from django.core.exceptions import ValidationError,  ObjectDoesNotExist 
from django.db.utils import IntegrityError
from .models import (
    CourseStudentMapping
)
from course.models import TeachersCoursesMapping
from course.serializer import TeachersCoursesMappingSerializer
from authentication.serializer import UserSerializer



class StudentDashboard(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        all_subjects = TeachersCoursesMapping.objects.active().select_related(
            "course", "teacher"
        )
        serializer = TeachersCoursesMappingSerializer(all_subjects, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class RegisterCourses(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    class CourseTeacherAllocatedSerializer(CourseStudentMappingSerializer):
        teacher = UserSerializer()

        class Meta(CourseStudentMappingSerializer.Meta):
            fields = CourseStudentMappingSerializer.Meta.fields + ["teacher"]

    def get(self, request):
        id = request.user.id
        all_registed_subject = CourseStudentMapping.objects.active().filter(student=id)
        serializer = self.CourseTeacherAllocatedSerializer(
            all_registed_subject, many=True
        )
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, pk):
        student = request.user
        try:
            teacher_course_mapping = TeachersCoursesMapping.objects.get(id=pk)
        except ObjectDoesNotExist as ex:
            return Response( {"message": str(ex)}, status.HTTP_404_NOT_FOUND)    
        teacher = teacher_course_mapping.teacher
        course = teacher_course_mapping.course
        student_course = CourseStudentMapping(
            student=student, course=course, teacher=teacher
        )
        try:
            student_course.save()
        except IntegrityError as ex:
            return Response({"message": str(ex)} , status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as ex: 
            return Response({"message": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"meassage": "Successfully registered"}, status.HTTP_200_OK)

class TeacherDashboard(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    class CourseStudentAllocatedSerializer(CourseStudentMappingSerializer):
        student = UserSerializer()

        class Meta(CourseStudentMappingSerializer.Meta):
            fields = CourseStudentMappingSerializer.Meta.fields + ["student"]

    def get(self, request):
        id = request.user.id
        student_list = CourseStudentMapping.objects.active().select_related(
            "teacher", "student", "course"
        ).filter(teacher__id=id)

        serializer = self.CourseStudentAllocatedSerializer(student_list, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


