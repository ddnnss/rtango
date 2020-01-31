# Generated by Django 3.0.2 on 2020-01-29 22:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_auto_20200129_2226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='material',
        ),
        migrations.RemoveField(
            model_name='item',
            name='subcategory',
        ),
        migrations.RemoveField(
            model_name='item',
            name='weight',
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ManyToManyField(db_index=True, to='item.Category', verbose_name='Состоит в категориях'),
        ),
        migrations.AlterField(
            model_name='item',
            name='filter',
            field=models.ManyToManyField(blank=True, db_index=True, to='item.Filter', verbose_name='Имеет фильтры'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 29, 22, 34, 3, 604776), verbose_name='Срок действия безлимитного кода'),
        ),
    ]