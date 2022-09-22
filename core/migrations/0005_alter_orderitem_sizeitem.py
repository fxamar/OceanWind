# Generated by Django 4.1.1 on 2022-09-17 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_orderitem_sizeitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='sizeItem',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.sizeitems', verbose_name='حجم ومقاس الصنف'),
        ),
    ]
