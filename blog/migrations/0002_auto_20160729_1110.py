# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-29 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=b'video', verbose_name=b'\xe8\xa7\x86\xe9\xa2\x91'),
        ),
    ]