from django.shortcuts import render
from king_admin import forms
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
    return render(request,'index.html')


@login_required
def customer_list(request):
    return render(request, 'sales/customer.html')


@login_required
def enrollment(request,obj_id):
    return render(request,'sales/enrollment.html')





