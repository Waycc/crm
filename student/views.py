from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'student/student.html')


def teacher_list(request):
    return render(request, 'student/teacher.html')
