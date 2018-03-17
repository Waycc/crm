from django.urls import path
from student import views


urlpatterns = [
    path('', views.index, name='stu_index'),
    path('teacher/', views.teacher_list, name='teacher_list')
]