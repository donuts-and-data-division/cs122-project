# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
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
                ('food_price', models.FloatField()),
                ('date_last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('food_type', models.CharField(default=0, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SnapLocations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.IntegerField()),
                ('double_value', models.BooleanField()),
                ('farmers_mkt', models.BooleanField()),
                ('store_name', models.CharField(max_length=5000)),
                ('address', models.CharField(max_length=5000)),
                ('place_id', models.CharField(max_length=5000)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('phone', models.CharField(max_length=5000)),
                ('hours', models.CharField(max_length=5000)),
                ('website', models.URLField(max_length=5000)),
                ('rating', models.CharField(max_length=5000)),
                ('store_category', models.CharField(max_length=5000)),
                ('price_level', models.CharField(max_length=5000)),
            ],
        ),
    ]
