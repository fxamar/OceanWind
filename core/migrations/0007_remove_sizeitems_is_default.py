# Generated by Django 4.1.1 on 2022-09-17 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_sizeitems_is_default'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sizeitems',
            name='is_default',
        ),
    ]