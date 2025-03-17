from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsStudent, IsTeacher
from rest_framework import status
from rest_framework.response import Response
from .serializer import (
    UserSerializer,
    CourseSerializer,
    TeachersCoursesMappingSerializer,
    CourseStudentMappingSerializer,
    GradeBookSerializer,
)
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import (
    Course,
    TeachersCoursesMapping,
    Course,
    CourseStudentMapping,
    GradeBook,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from .exception import CustomException
from rest_framework.views import APIView

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "id": user.id,
        "role": user.role,
    }


class RegisrationSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["password"]


@api_view(["POST"])
def register(request):
    try:
        if request.method == "POST":
            if not request.data.get("role").lower() in ["admin", "student"]:  # allowed roles
                raise CustomException("only admin and students are allowed")
            user = RegisrationSerializer(data=request.data)
            if not (user.is_valid()):
                raise CustomException("data not correct")
            user.save()
            return Response({"message": "successfully registered"}, status.HTTP_200_OK)
    except CustomException as ex:

        message = {"message": str(ex)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        message = {"message": "Something wemt wrong"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET", "POST"])
def teacher_register(request):
    try:
        if request.method == "POST":
            # transaction atomic should for specific code
            with transaction.atomic():
                if request.data.get("role").lower() != "teacher":
                    raise CustomException("role should be teacher")
                user = RegisrationSerializer(
                    data={
                        "username": request.data.get("username"),
                        "password": request.data.get("password"),
                        "role": request.data.get("role"),
                    }
                )

                if not (user.is_valid()):
                    raise CustomException("date not correct")
                user.save()
                for i in request.data.get("subject"):
                    teacher = User.objects.filter(
                        username=request.data.get("username")
                    ).first()
                    course = Course.objects.filter(name=i).first()
                    teacher_course_mapping = TeachersCoursesMapping(
                        teacher=teacher, course=course
                    )
                    teacher_course_mapping.save()
                return Response(
                    {"message": "successfully registered"}, status.HTTP_200_OK
                )
    except CustomException as ex:
        message = {"message": str(ex)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        message = {"meessage": "Somthing went wrong"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def login(request):
    if request.method == "POST":
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = User.objects.filter(username=username).first()
            if not user:
                raise CustomException("user does not exist")
            elif check_password(password, user.password):
                tokens = get_tokens_for_user(user)
            else:
                raise CustomException("unauthorised")
            return Response(tokens, status.HTTP_200_OK)
        except CustomException as ex:
            message = {"message": str(ex)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            message = {"message": "Somthing went wrong"}
            return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdmin])
def add_course(request):
    try:
        serializer_add_course = CourseSerializer(data=request.data)
        if not (serializer_add_course.is_valid()):
            raise CustomException("date not correct")
        serializer_add_course.save()
        return Response(serializer_add_course.data, status.HTTP_200_OK)
    except CustomException as ex:
            message = {"message": str(ex)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        message = {"message": "Something went wrong"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdmin])
def update_course(request, pk):
    # try exception implementation and get
    try:
        if request.method == "PUT":
            course = Course.objects.get(id=pk)
            serializer_update_course = CourseSerializer(
                instance=course, data=request.data
            )
            if not (serializer_update_course.is_valid()):
                raise CustomException("data not correct")
            serializer_update_course.save()
        return Response(serializer_update_course.data, status.HTTP_200_OK)
    except CustomException as ex:
            message = {"message": str(ex)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        message = {"meassage": "Something went wrong"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdmin])
def delete_course(request, pk):
    try:
        course = Course.objects.get(id=pk)
        course.delete()
        return Response({"message": "successfully deleted"}, status.HTTP_200_OK)
    except Exception as ex:
        # error that can come in deletion
        message = {"message": "Resourse Does not exists"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def dashboard(request):
    try:
        all_subjects = TeachersCoursesMapping.objects.select_related(
            "course", "teacher"
        ).all()
        serializer = TeachersCoursesMappingSerializer(all_subjects, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    except Exception as ex:
        message = {"message": "Something went wrong"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsStudent])
def register_course(request, pk):
    try:
        student = request.user
        teacher_course_mapping = TeachersCoursesMapping.objects.get(id=pk)
        teacher = teacher_course_mapping.teacher
        course = teacher_course_mapping.course
        # can you do this without object
        student_course = CourseStudentMapping(
            student=student, course=course, teacher=teacher
        )
        student_course.save()
        return Response({"meassage": "successfully registered"}, status.HTTP_200_OK)
    except Exception as ex:
        message = {"message": "Something went wrong"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def get_registered_course(request):
    try:
        id = request.user.id
        all_registed_subject = CourseStudentMapping.objects.filter(student=id)

        class CourseTeacherAllocatedSerializer(CourseStudentMappingSerializer):
            teacher = UserSerializer()

            class Meta(CourseStudentMappingSerializer.Meta):
                fields = CourseStudentMappingSerializer.Meta.fields + ["teacher"]

        serializer = CourseTeacherAllocatedSerializer(all_registed_subject, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    except Exception as ex:
        message = {"message": "Something went wrong"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsTeacher])
def get_techer_courses(request):
    try:
        id = request.user.id
        student_list = CourseStudentMapping.objects.select_related(
            "teacher"
        ).filter(teacher__id=id)

        class CourseStudentAllocatedSerializer(CourseStudentMappingSerializer):
            student = UserSerializer()

            class Meta(CourseStudentMappingSerializer.Meta):
                fields = CourseStudentMappingSerializer.Meta.fields + ["student"]

        serializer = CourseStudentAllocatedSerializer(student_list, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    except Exception:
        message = {"message": "Something went wrong"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


# only teacher can access
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsTeacher])
def update_gradebook(request):
    try:
        with transaction.atomic():
            id = request.user.id
            class ValidateInputDataGradeBookSerialier(serializers.Serializer):
                student_id = serializers.IntegerField(required=True)
                course_id = serializers.IntegerField(required=True)
                marks_obtained = serializers.FloatField(required=True, min_value=0.0, max_value=100.0)
                passing_marks = serializers.FloatField(required=True, min_value=0.0, max_value=100.0)

            validate_input_data =  ValidateInputDataGradeBookSerialier(data = request.data) 
            if not (validate_input_data.is_valid()):
                raise CustomException("data not correct")   

            student_id = int(request.data.get("student_id"))
            course_id = int(request.data.get("course_id"))
            # TODO filter query
            course_student_queryset = (
                CourseStudentMapping.objects
                .select_related("teacher")
                .filter(teacher__id=id , course = course_id , student = student_id )
            )
            if not course_student_queryset:
                raise CustomException("Student Course alloaction not found")
            for course_student_obj in course_student_queryset:
                grade_book = GradeBook(
                    course=course_student_obj.course,
                    marks_obtained=float(request.data.get("marks_obtained")),
                    passing_marks=float(request.data.get("passing_marks")),
                    student=course_student_obj.student,
                )
                grade_book.save()
                course_student_obj.status = "Completed"
                course_student_obj.save()
        return Response({"meassage": "successfully added Grade"}, status.HTTP_200_OK)
    except CustomException as ex:
            message = {"message": str(ex)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        message = {"message": "Something went wrong"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def get_gradebook(request):
    try:
        id = request.user.id
        grade_book = GradeBook.objects.select_related("course", "student").filter(
            student=id
        )
        serializer = GradeBookSerializer(grade_book, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    except Exception as ex:
        message = {"message": "Something went wrong"}
        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)
