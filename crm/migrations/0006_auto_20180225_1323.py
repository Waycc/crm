# Generated by Django 2.0.1 on 2018-02-25 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_menu_url_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(help_text='<a>修改密码</a>', max_length=128, verbose_name='password'),
        ),
    ]
