# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-11 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20171211_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='development',
            name='activity_description',
        ),
        migrations.RemoveField(
            model_name='development',
            name='application_title',
        ),
        migrations.RemoveField(
            model_name='development',
            name='environmental_assessment_practitioner',
        ),
        migrations.RemoveField(
            model_name='development',
            name='environmental_consultancy',
        ),
        migrations.AddField(
            model_name='permit',
            name='activity_description',
            field=models.TextField(blank=True, help_text="Provides more detail on what the development will entail, e.g. 'The development proposal will comprise of the following: Residential, internal roads, and access control.'", null=True),
        ),
        migrations.AddField(
            model_name='permit',
            name='application_title',
            field=models.CharField(blank=True, help_text="Should describe what the development is, e.g. 'Establishment of the Northern Golf Course Estate, Johannesburg Gauteng'.", max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='permit',
            name='environmental_assessment_practitioner',
            field=models.CharField(blank=True, help_text='The name of the staff member in the above consultancy.', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='permit',
            name='environmental_consultancy',
            field=models.CharField(blank=True, help_text='The name of the consultancy who performed the EIA', max_length=100, null=True),
        ),
    ]
