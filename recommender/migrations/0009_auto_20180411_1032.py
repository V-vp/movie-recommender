# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-11 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0008_auto_20180409_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieinfo',
            name='awards',
            field=models.CharField(default='niull', max_length=1500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movieinfo',
            name='user_rating',
            field=models.IntegerField(default=0),
        ),
    ]
