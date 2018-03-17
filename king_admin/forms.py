from django.forms import ModelForm
from django.core.exceptions import ValidationError
from crm import models


class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'



def create_model_form(admin_class):

    def __new__(cls,*args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
            if hasattr(admin_class,'is_add_form') and hasattr(admin_class,'readonly_fields'):
                if field_name in admin_class.readonly_fields and not admin_class.is_add_form:
                    field_obj.widget.attrs['disabled'] = 'disabled'

        return ModelForm.__new__(cls)

    def default_clean(self):
        if self.instance.id:
            error_list = []
            if hasattr(admin_class,'readonly_fields'):
                for field in admin_class.readonly_fields:
                    data_from_front = self.cleaned_data[field]
                    data_from_db = getattr(self.instance, field)
                    if hasattr(data_from_db, 'all'):
                        m2m_objs = getattr(data_from_db, 'all')()  #相当于self.instance.tags.all()
                        id_from_db = set(i[0] for i in m2m_objs.values_list())
                        id_from_front = set(i.id for i in self.cleaned_data.get(field))
                        if id_from_front != id_from_db:
                            error_list.append(ValidationError('%s字段不能修改'%field))

                    else:
                        if data_from_front !=data_from_db:
                            error_list.append(ValidationError('%s字段不能修改' % field))
                if error_list:
                    raise ValidationError(error_list)


        return self.cleaned_data


    class Meta:
        model = admin_class.model
        fields = '__all__'
        exclude = admin_class.modelform_exclude_fields

    fun_dict = {'Meta': Meta, '__new__':__new__,'clean':default_clean}
    model_form_class = type('DynamicModelForm', (ModelForm,), fun_dict)

    return model_form_class