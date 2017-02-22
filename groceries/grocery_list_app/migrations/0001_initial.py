# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=100)),
                ('food_quantity', models.CharField(max_length=20)),
                ('food_price', models.CharField(max_length=6)),
                ('date_last_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
