from django.urls import path
from . import views


urlpatterns = [
    path('teacher' , view= views.UpdateGradeBook.as_view()  , name = 'update-gradebook' ),
    path('student' , view= views.GetGradeBook.as_view() , name = 'get-gradebook' )
]
