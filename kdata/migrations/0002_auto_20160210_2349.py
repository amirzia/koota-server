# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kdata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_id',
            field=models.CharField(max_length=64, primary_key=True, serialize=False, unique=True),
        ),
    ]