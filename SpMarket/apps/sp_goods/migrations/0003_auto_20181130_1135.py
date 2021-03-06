# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 11:35
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sp_goods', '0002_category_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityzone',
            options={'verbose_name': '活动专区管理', 'verbose_name_plural': '活动专区管理'},
        ),
        migrations.AlterModelOptions(
            name='banner',
            options={'verbose_name': '轮播管理', 'verbose_name_plural': '轮播管理'},
        ),
        migrations.AlterField(
            model_name='goodsspu',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='商品详情'),
        ),
    ]
