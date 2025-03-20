from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import ValidationError 
from django.db import transaction 
from django.db.utils import IntegrityError
from course.models import Course , TeachersCoursesMapping
from .models import (
    User
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "id": user.id,
        "role": user.role,
    }


class Register(APIView):
    class RegistrationSerializer(serializers.Serializer):
        username = serializers.CharField(required=True)
        password = serializers.CharField(required=True)
        role  = serializers.CharField(required=True)

    def post(self, request):
        if not request.data.get("role").lower() in ["admin", "student"]:
            return Response({"message": "Only admin and students are allowed"}, status=status.HTTP_400_BAD_REQUEST)
        user = self.RegistrationSerializer(data=request.data)
        if not user.is_valid():
            return Response({"message": user.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            User.objects.create_user(
                username=user.validated_data.get("username"),
                password=user.validated_data.get("password"),
                role=user.validated_data.get("role"),
            )
            return Response({"message": "Successfully registered"}, status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        


class TeacherRegister(APIView):

    class RegistrationSerializer(serializers.Serializer):
        username = serializers.CharField(required=True)
        password = serializers.CharField(required=True)
        role  = serializers.CharField(required=True)

    def post(self, request):
        # transaction atomic should for specific code
        if request.data.get("role").lower() != "teacher":
            return Response( {"message": "Role should be teacher"}, status=status.HTTP_400_BAD_REQUEST)
        user = self.RegistrationSerializer(
            data={
                "username": request.data.get("username"),
                "password": request.data.get("password"),
                "role": request.data.get("role"),
            }
        )

        if not user.is_valid():
            return Response( {"message": user.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                teacher = User.objects.create_user(
                    username=user.validated_data.get("username"),
                    password=user.validated_data.get("password"),
                    role=user.validated_data.get("role"),
                )

                for subject in request.data.get("subjects"):
                    course = Course.objects.active().filter(name=subject).first()
                    if not course:
                        return Response( {"message": "Course does not exists"}, status=status.HTTP_404_NOT_FOUND)
                    teacher_course_mapping = TeachersCoursesMapping(
                        teacher=teacher, course=course
                    )
                    teacher_course_mapping.save()
        except IntegrityError as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)   
        except ValidationError as ex:
            return Response({"message": ex.message}, status=status.HTTP_400_BAD_REQUEST) 
                
        return Response(
            {"message": "Successfully registered"}, status.HTTP_200_OK
        )


class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.active().filter(username=username).first() #do we need here
        if not user:
            return Response( {"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        elif check_password(password, user.password):
            tokens = get_tokens_for_user(user)
        else:
            return Response( {"message": "Unauthoried"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(tokens, status.HTTP_200_OK)
