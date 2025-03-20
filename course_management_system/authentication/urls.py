from django.urls import path
from . import views

urlpatterns = [
    path('registration', view=views.Register.as_view() , name = "register"),
    path('registration-teacher', view=views.TeacherRegister.as_view() , name = "teacher_register"), 
    path('login', view=views.Login.as_view() , name = "login"), 
]
