# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-01 19:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sp_order', '0003_auto_20181130_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='商品的总价格'),
        ),
    ]
