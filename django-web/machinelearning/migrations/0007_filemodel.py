# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machinelearning', '0006_auto_20170319_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='FILEMODEL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='upload/%Y%m%d')),
            ],
        ),
    ]
