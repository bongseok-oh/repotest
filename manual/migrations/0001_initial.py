# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-09 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompareWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tester', models.CharField(max_length=255, null=True)),
                ('origin', models.FileField(upload_to='')),
                ('result', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='WordDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255, null=True)),
                ('desc', models.CharField(max_length=255, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
