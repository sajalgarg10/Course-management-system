from django.urls import path
from . import views

urlpatterns = [
    path('add' , view= views.CourseView.as_view() , name = 'add' ),
    path('<int:pk>' , view= views.CourseView.as_view() , name = 'course' ),
]
