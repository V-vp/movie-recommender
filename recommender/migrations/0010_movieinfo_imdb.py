# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-11 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0009_auto_20180411_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieinfo',
            name='imdb',
            field=models.IntegerField(default=0),
        ),
    ]
