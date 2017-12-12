# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-12 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20171212_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offsettrigger',
            name='type_of_trigger',
            field=models.CharField(choices=[('E', 'Ecosystem'), ('T', 'Threatened or protected species')], max_length=1),
        ),
    ]
