# Generated by Django 3.0.2 on 2020-02-09 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0005_auto_20200204_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='comment',
        ),
        migrations.AddField(
            model_name='item',
            name='page_text',
            field=models.TextField(blank=True, null=True, verbose_name='СЕО Текст на странице'),
        ),
    ]