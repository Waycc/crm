from crm import models
from django.shortcuts import render,redirect

enable_admin = {}  # {'crm':{'model_name':admin_class}}

class BaseAdmin(object):
    list_display = ()
    list_filter = ()
    search_fields = ()
    raw_id_fields = ()
    filter_horizontal = ()
    list_editable = ()
    per_page = 4
    action = ('delete_selected_objs',)
    modelform_exclude_fields = ()

    def delete_selected_objs(self,request,delete_obj):
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        if request.POST.get('confirm') == 'yes':
            delete_obj.delete()
            return redirect('/king_admin/%s/%s/'%(app_name,table_name))
        selected_id_list = ','.join([str(i.id) for i in delete_obj])


        return render(request,'king_admin/table_objs_delete.html',{'delete_obj':delete_obj,
                                                                   'request':request,
                                                                   'app_name':app_name,
                                                                   'table_name':table_name,
                                                                   'selected_id_list':selected_id_list,
                                                                   'action':request._action
                                                                   })


class CustomerAdmin(BaseAdmin):
    list_display = ('id', 'name','qq', 'source', 'consultant', 'consult_course', 'date', 'status','报名')
    list_filter = ('source', 'consultant', 'consult_course', 'status', 'date')
    search_fields = ('qq','name','consultant__name')
    filter_horizontal = ('tags',)
    action = ('delete_selected_objs',)
    readonly_fields = ["qq", "consultant", "tags"]


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer', 'consultant', 'date')
    list_filter = ('customer', 'consultant', 'date')
    search_fields = ('customer__qq', 'consultant__name')


class UserProfileAdmin(BaseAdmin):
    list_display = ('email', 'name')
    filter_horizontal = ('user_permissions', 'groups',)
    readonly_fields = ('password',)
    modelform_exclude_fields = ('last_login',)


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enable_admin:
        enable_admin[model_class._meta.app_label] = {}

    admin_class.model = model_class
    enable_admin[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
register(models.UserProfile, UserProfileAdmin)
