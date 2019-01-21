# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-08 13:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommender', '0002_auto_20180408_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieinfo',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
