# Generated by Django 2.2.7 on 2020-02-04 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordershipping',
            name='price',
            field=models.IntegerField(null=True, verbose_name='Стоимость доставки'),
        ),
    ]
