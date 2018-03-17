from django.db.models import Q
from django.shortcuts import HttpResponse
from django.urls import resolve



def table_filter(request,admin_class):
    filter_dict = {}  #前端传回的键值对
    real_filter_condition = {}   #真正用来查询的键值对

    for k,v in request.GET.items():

        if v and k in admin_class.list_filter:
            field_obj = admin_class.model._meta.get_field(k)
            filter_dict[k] = v
            if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
                k = '%s__gt'%k
            real_filter_condition[k] = v
    print(filter_dict)
    obj_list = admin_class.model.objects.filter(**real_filter_condition)
    return obj_list, filter_dict


def table_sort(request,object_list):
    order_field = request.GET.get('o')
    if order_field:
        if order_field.startswith('-'):
            object_list = object_list.order_by(order_field)
            order_field = order_field.strip('-')
        else:
            object_list = object_list.order_by(order_field)
            order_field = '-%s'%order_field

    return object_list,order_field


def table_search(request, object_list, admin_class):
    search_key = request.GET.get('search_key','')
    q_obj = Q()
    q_obj.connector = 'OR'
    if search_key:
        for search_field in admin_class.search_fields:
            q_obj.children.append(('%s__contains'%search_field, search_key))
            res = object_list.filter(q_obj)
            for obj in res:
                print(obj.id)
    res = object_list.filter(q_obj)

    return res


def check_permission(func):
    '''验证用户是否具有权限'''
    def wrap(request,*arg,**kwargs):
        roles = request.user.roles
        resolved_url_name = resolve(request.path).url_name
        print(resolved_url_name)
        if roles.filter(permission__url_name=resolved_url_name):
            return func(request, *arg, **kwargs)
        else:
            return HttpResponse('没有权限')
    return wrap




