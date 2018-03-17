from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime, timedelta
from django.core.exceptions import FieldDoesNotExist

register = template.Library()

@register.simple_tag
def table_name(admin_class):
    return admin_class.model._meta.verbose_name


@register.simple_tag
def return_model_obj(admin_class):
    return admin_class.model.objects.all()

@register.simple_tag
def field_data(request, obj, admin_class):
    td = ''
    for index, field in enumerate(admin_class.list_display):
        try:
            field_obj = obj._meta.get_field(field)    #取得字段对象
            if field_obj.choices:
                field_datas = getattr(obj, 'get_%s_display'%field)()   #获取字段中choice内容的值
            else:
                field_datas = getattr(obj, field)
                if field_datas is None:
                    field_datas = '  '
            if type(field_datas).__name__ == 'datetime':
                field_datas = field_datas.strftime("%Y-%m-%d %H:%M:%S")
            if index == 0:
                field_datas = '<a href="{request_path}{obj_id}/change/">{field_datas}</a>'.format(request_path=request.path,
                                                                                                  obj_id=obj.id,
                                                                                                  field_datas=field_datas
                                                                                                  )
        except FieldDoesNotExist:
            field_datas = '<a href="/crm/customer/%s/enrollment/">报名</a>'%obj.id
        td += '<td>%s</td>'%field_datas
    return mark_safe(td)


def return_page_range(num_pages, current_page):
    '''分页用的'''
    if current_page < 5 :
        if num_pages<10:
            page_range = range(1,num_pages+1)
        else:
            page_range = range(1, 10)
    else:
        if current_page > num_pages-5:
            if num_pages-8 <= 0:
                page_range = range(1,num_pages+1)
            else:
                page_range = range(num_pages-8, num_pages+1)
        else:
            page_range = range(current_page-4, current_page+5)
    return page_range


@register.simple_tag
def return_page_ele(query_set,filter_dict,request):
    ele = ''
    num_pages = query_set.paginator.num_pages    #总页数
    current_page = query_set.number   # 当前页
    page_range = return_page_range(num_pages,current_page)
    o = request.o
    search_key = request.search_key
    # page_range = range(1,query_set.paginator.num_pages+1)
    #print(query_set.paginator.num_pages)
    filter_condition = ''
    for k, v in filter_dict.items():
        filter_condition += '%s=%s&' % (k, v)
    for page in page_range:

        if page == query_set.number:
            ele += '<li class="active"><a href="?page=%s&%so=%s&search_key=%s">%s</a><li>'%(page, filter_condition,
                                                                               o,search_key, page)

        else:

            ele += '<li class=""><a href="?page=%s&%so=%s&search_key=%s">%s</a><li>'%(page, filter_condition,
                                                                               o,search_key, page)
    return mark_safe(ele)


@register.simple_tag
def return_option_ele(filter_condition, admin_class, filter_dict):
    select_ele = '<option value=''>----</option>'
    field_obj = admin_class.model._meta.get_field(filter_condition)
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            #print("choice", choice_item, filter_dict.get(filter_condition), type(filter_dict.get(filter_condition)))
            if filter_dict.get(filter_condition) == str(choice_item[0]):
                selected = "selected"

            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]: # [('', '---------'), (1, 'Wei'), (2, 'alex')]
            if filter_dict.get(filter_condition) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''

    if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
        date_list = [('一个月内',datetime.now()-timedelta(days=30)),
                      ('10天内',datetime.now()-timedelta(days=10)),
                     ('2天内',datetime.now()-timedelta(days=2))]
        filter_dict_time_str = filter_dict.get(filter_condition, '')

        compare_time = timedelta(seconds=60)
        for date_data in date_list:
            try:
                filter_dict_time = datetime.strptime(filter_dict_time_str, '%Y-%m-%d %H:%M:%S.%f')
            except Exception:
                filter_dict_time = date_data[1] - timedelta(days=1)
            if date_data[1] - filter_dict_time < compare_time:
                selected = "selected"
            else:
                selected = ''
            select_ele += '<option value="%s" %s>%s</option>' %(date_data[1],selected,date_data[0])

    # select_ele += "</select>"
    return mark_safe(select_ele)
    # ele = '<option>---</option>'
    # filters = admin_class.model.objects.all()
    # field = admin_class.model._meta.get_field(filter_condition)
    # for obj in filters:
    #     if field.choices:
    #         filters_data = getattr(obj,'get_%s_display'%filter_condition)()
    #         ele+='<option>%s</option>'%filters_data
    #         # print(filters_data)
    # for select in filters:
    #     ele+= select


@register.simple_tag
def return_filter_condition(filter_dict):
    filter_condition = ''
    for k, v in filter_dict.items():
        filter_condition += '%s=%s&' % (k, v)
    return mark_safe(filter_condition)


@register.simple_tag
def get_order_field_ele(field, order_field, filter_dict, admin_class):
    a_ele = '<a href=?{filters}o={order_field}>{field}</a>{icon_ele}'
    filter_condition = ''
    for k, v in filter_dict.items():
        filter_condition += '%s=%s&' % (k, v)

    if order_field:
        if order_field.startswith('-'):
            icon_ele = '<span class="glyphicon glyphicon-chevron-up"></span>'
        else:
            icon_ele = '<span class="glyphicon glyphicon-chevron-down"></span>'
        if order_field.strip('-') == field:
            order_field = order_field
        else:
            order_field =field
            icon_ele = ''
    else:
        order_field = field
        icon_ele = ''

    try:
        verbose_name = admin_class.model._meta.get_field(field).verbose_name
        field_name = verbose_name
    except FieldDoesNotExist:
        field_name = field
        a_ele = '<a href="javascript:void(0);">{field}</a>'.format(field=field_name)

    a_ele = a_ele.format(filters=filter_condition, order_field=order_field, icon_ele=icon_ele, field=field_name)
    return mark_safe(a_ele)


# @register.simple_tag
# def get_order_field(field, order_field):
#     if order_field:
#         if order_field.strip('-') == field:
#             order_field = order_field
#         else:
#             order_field =field
#     else:
#         order_field = field
#     return order_field
#
#
# @register.simple_tag
# def get_icon(field_status,field,order_field):
#     if field_status.startswith('-'):
#         sort_icon = '<span class="glyphicon glyphicon-chevron-up"></span>'
#     else:
#         sort_icon = '<span class="glyphicon glyphicon-chevron-down"></span>'
#     if order_field.strip('-') != field:
#         sort_icon = ''
#     return mark_safe(sort_icon)


@register.simple_tag
def return_m2m_obj(admin_class, field, model_form_obj):
    field_obj = getattr(admin_class.model, field.name) #拿到tags对象
    field_obj_list = field_obj.rel.model.objects.all()   #拿到tags所有数据对象
    standby_obj_list = []
    if model_form_obj.instance.id:
        instance_obj = getattr(model_form_obj.instance, field.name)  #当前要修改的对象
        selected_obj_list = instance_obj.all()
    else:
        return field_obj_list

    for obj in field_obj_list:
        if obj not in selected_obj_list:
            standby_obj_list.append(obj)


    return standby_obj_list


@register.simple_tag
def return_selected_obj(field,model_form_obj):

    if model_form_obj.instance.id:

        instance_obj = getattr(model_form_obj.instance, field.name)
        selected_obj_list = instance_obj.all()
        return selected_obj_list


@register.simple_tag
def recursive_related_objs_lookup(objs):
    #model_name = objs[0]._meta.model_name
    ul_ele = "<ul>"
    for obj in objs:
        li_ele = '''<li> %s: %s </li>'''%(obj._meta.verbose_name,obj.__str__().strip("<>"))
        ul_ele += li_ele

        #for local many to many
        #print("------- obj._meta.local_many_to_many", obj._meta.local_many_to_many)
        for m2m_field in obj._meta.local_many_to_many: #把所有跟这个对象直接关联的m2m字段取出来了
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj,m2m_field.name) #getattr(customer, 'tags')
            for o in m2m_field_obj.select_related():# customer.tags.select_related()
                li_ele = '''<li> %s: %s </li>''' % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul_ele +=li_ele

            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele  #最终跟最外层的ul相拼接


        for related_obj in obj._meta.related_objects:
            if 'ManyToManyRel' in related_obj.__repr__():
                if hasattr(obj, related_obj.get_accessor_name()):  # hassattr(customer,'enrollment_set')
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    print("-------ManyToManyRel",accessor_obj,related_obj.get_accessor_name())
                    # 上面accessor_obj 相当于 customer.enrollment_set
                    if hasattr(accessor_obj, 'select_related'):  # slect_related() == all()
                        target_objs = accessor_obj.select_related()  # .filter(**filter_coditions)
                        # target_objs 相当于 customer.enrollment_set.all()

                        sub_ul_ele ="<ul style='color:red'>"
                        for o in target_objs:
                            li_ele = '''<li> %s: %s </li>''' % (o._meta.verbose_name, o.__str__().strip("<>"))
                            sub_ul_ele += li_ele
                        sub_ul_ele += "</ul>"
                        ul_ele += sub_ul_ele

            elif hasattr(obj,related_obj.get_accessor_name()): # hassattr(customer,'enrollment_set')
                accessor_obj = getattr(obj,related_obj.get_accessor_name())
                #上面accessor_obj 相当于 customer.enrollment_set
                if hasattr(accessor_obj,'select_related'): # slect_related() == all()
                    target_objs = accessor_obj.select_related() #.filter(**filter_coditions)
                    # target_objs 相当于 customer.enrollment_set.all()
                else:
                    print("one to one i guess:",accessor_obj)
                    target_objs = accessor_obj

                if len(target_objs) >0:
                    #print("\033[31;1mdeeper layer lookup -------\033[0m")
                    #nodes = recursive_related_objs_lookup(target_objs,model_name)
                    nodes = recursive_related_objs_lookup(target_objs)
                    ul_ele += nodes
    ul_ele +="</ul>"
    return ul_ele


@register.simple_tag
def display_obj_related(objs):
    '''把对象及所有相关联的数据取出来'''
    #objs = [objs,] #fake
    if objs:
        model_class = objs[0]._meta.model
        mode_name = objs[0]._meta.model_name
        return mark_safe(recursive_related_objs_lookup(objs))

