from django.urls import path
from . import views
from . import views2

urlpatterns = [
    path('registration', view=views2.Register.as_view() , name = "register"),
    path('registration-teacher', view=views2.TeacherRegister.as_view() , name = "teacher_register"), 
    path('login', view=views2.Login.as_view() , name = "login"), 
    path('add-course' , view= views2.CourseView.as_view() , name = 'add' ),
    path('course/<int:pk>' , view= views2.CourseView.as_view() , name = 'course' ),
    # path('course/<int:pk>' , view= views2.CourseView.as_view() , name = 'delete' ),
    path('student-dashboard' , view= views2.StudentDashboard.as_view() , name = 'teachers' ),
    path('teacher-dashboard' , view= views2.TeacherDashboard.as_view() , name = 'students' ),
    path('register-course/teacher-course-mapping/<int:pk>' , view= views2.RegisterCourses.as_view() , name = 'register-course' ),
    path('registered-courses' , view= views2.RegisterCourses.as_view()  , name = 'registered-courses' ),
    path('gradebook/teacher' , view= views2.UpdateGradeBook.as_view()  , name = 'update-gradebook' ),
    path('gradebook/student' , view= views2.GetGradeBook.as_view() , name = 'get-gradebook' )
]
