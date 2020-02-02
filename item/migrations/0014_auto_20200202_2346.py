# Generated by Django 3.0.2 on 2020-02-02 23:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0013_auto_20200202_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 2, 23, 46, 14, 318406), verbose_name='Срок действия безлимитного кода'),
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topText', models.CharField(max_length=25, null=True, verbose_name='Заголовок')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('expiry', models.CharField(max_length=25, null=True, verbose_name='Окончание акции (в формате год/месяц/день)')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='item.Item', verbose_name='Букет')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
            },
        ),
    ]
