# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-09 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manual', '0003_auto_20180109_1354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compareword',
            old_name='origin',
            new_name='origin_file',
        ),
        migrations.AddField(
            model_name='compareword',
            name='desc',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compareword',
            name='result_file',
            field=models.FileField(blank=True, null=True, upload_to='manual/%Y/%m/%d'),
        ),
    ]
