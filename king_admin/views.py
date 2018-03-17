from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from MyCRM.utils import *
from king_admin import myadmin, forms


# Create your views here.





@login_required
@check_permission
def index(request):
    enable_admin = myadmin.enable_admin
    return render(request, 'king_admin/index.html', {'enable_admin':enable_admin})



@login_required
@check_permission
def display_table_objs(request, app_name, table_name):
    admin_class = myadmin.enable_admin[app_name][table_name]
    # obj_list = admin_class.model.objects.all()
    if request.method == 'POST':
        selected_id_list = request.POST.get('selected_id_list')
        action = request.POST.get('action_select','')
        request._action = action
        if selected_id_list:
            delete_obj = admin_class.model.objects.filter(id__in=selected_id_list.split(','))
            if hasattr(admin_class, action):
                action_func = getattr(admin_class, action)
                return action_func(admin_class, request,delete_obj)

    obj_list, filter_dict = table_filter(request,admin_class)

    obj_list = table_search(request, obj_list,admin_class)
    obj_list, order_field = table_sort(request, obj_list)
    paginator = Paginator(obj_list, admin_class.per_page)
    page = request.GET.get('page')
    request.o= request.GET.get('o','')
    request.search_key = request.GET.get('search_key', '')
    try:
        query_set = paginator.page(page)
    except PageNotAnInteger:
        query_set = paginator.page(1)
    except EmptyPage:
        query_set = paginator.page(paginator.num_pages)

    return render(request,'king_admin/table_objs.html', {'admin_class': admin_class,
                                                         'request':request,
                                                         'query_set':query_set,
                                                         'filter_dict':filter_dict,
                                                         'order_field':order_field,
                                                         })



@login_required
@check_permission
def table_objs_add(request,app_name, table_name):
    admin_class = myadmin.enable_admin[app_name][table_name]
    model_form_class = forms.create_model_form(admin_class)
    admin_class.is_add_form = True

    if request.method == 'POST':
        model_form_obj = model_form_class(request.POST)
        if model_form_obj.is_valid():
            model_form_obj.save()
            return redirect(request.path.replace('/add/','/'))
    else:
        model_form_obj = model_form_class()

    return render(request,'king_admin/table_objs_add.html',{'model_form_obj':model_form_obj,
                                                               'admin_class':admin_class})



@login_required
@check_permission
def table_objs_change(request,app_name, table_name, obj_id):
    admin_class = myadmin.enable_admin[app_name][table_name]
    admin_class.is_add_form = False
    model_form_class = forms.create_model_form(admin_class)
    obj = admin_class.model.objects.filter(id=obj_id).first()
    if request.method == 'POST':
        model_form_obj = model_form_class(request.POST, instance=obj)
        if model_form_obj.is_valid():
            model_form_obj.save()
    else:
        model_form_obj = model_form_class(instance=obj)
    return render(request,'king_admin/table_objs_change.html',{'model_form_obj':model_form_obj,
                                                               'admin_class':admin_class,
                                                               'app_name':app_name,
                                                               'table_name':table_name,
                                                               })



@login_required
@check_permission
def table_objs_delete(request,app_name,table_name,obj_id):
    admin_class = myadmin.enable_admin[app_name][table_name]
    delete_obj = admin_class.model.objects.filter(id=obj_id)
    if request.method == 'POST':
        delete_obj.delete()
        return redirect('/king_admin/%s/%s/'%(app_name,table_name))

    return render(request,'king_admin/table_objs_delete.html',{'delete_obj':delete_obj,
                                                               'app_name':app_name,
                                                               'table_name':table_name
                                                               })



def test(request):
    from . import forms
    f = forms.CustomerModelForm(initial={'name': 'wa'})
    return render(request,'test.html',{'f':f})
