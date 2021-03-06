# Generated by Django 2.2.7 on 2020-02-03 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок отображения')),
                ('image', models.ImageField(upload_to='banners/', verbose_name='Картинка (1920x680)')),
                ('is_active', models.BooleanField(default=True)),
                ('text_top', models.CharField(blank=True, max_length=50, null=True, verbose_name='Заголовок 1')),
                ('text_middle', models.CharField(blank=True, max_length=50, null=True, verbose_name='Заголовок 2')),
                ('text_bottom', models.CharField(blank=True, max_length=50, null=True, verbose_name='Заголовок 3')),
                ('text_button', models.CharField(blank=True, max_length=10, null=True, verbose_name='Надпись на кнопке')),
                ('url', models.CharField(blank=True, max_length=255, verbose_name='Ссылка с кнопки')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
            },
        ),
        migrations.CreateModel(
            name='OneClick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='item.Item', verbose_name='Букет')),
            ],
            options={
                'verbose_name': 'Покупка в 1 клик',
                'verbose_name_plural': 'Покупки в 1 клик',
            },
        ),
    ]
