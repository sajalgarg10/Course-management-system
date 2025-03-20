from django.urls import path
from . import views

urlpatterns = [
    path('student' , view= views.StudentDashboard.as_view() , name = 'teachers' ),
    path('teacher' , view= views.TeacherDashboard.as_view() , name = 'students' ),
    path('register-course/teacher-course-mapping/<int:pk>' , view= views.RegisterCourses.as_view() , name = 'register-course' ),
    path('registered-courses' , view= views.RegisterCourses.as_view()  , name = 'registered-courses' ),
]
