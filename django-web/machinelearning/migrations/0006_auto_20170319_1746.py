# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 09:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('machinelearning', '0005_remove_file_file'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FILE',
            new_name='TOPIC',
        ),
    ]
