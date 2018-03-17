from django.urls import path
from django.conf.urls import url
from crm import views


urlpatterns = [
    path('', views.index, name='sales_index'),
    url(r'customer/(\d+)/enrollment', views.enrollment, name='enrollment'),
    path('customer/', views.customer_list, name='customer_list'),


]