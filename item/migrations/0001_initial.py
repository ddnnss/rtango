# Generated by Django 2.2.7 on 2020-02-03 11:22

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название категории')),
                ('name_slug', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, upload_to='category_img/', verbose_name='Изображение категории 370x150')),
                ('page_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название страницы')),
                ('page_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание страницы')),
                ('page_keywords', models.TextField(blank=True, null=True, verbose_name='Keywords')),
                ('short_description', models.TextField(blank=True, verbose_name='Краткое описание для главной')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание категории')),
                ('show_at_index', models.BooleanField(default=False, verbose_name='Показывать на главной?')),
                ('show_at_main_menu', models.BooleanField(default=False, verbose_name='Показывать в главном меню отдельной категорией?')),
                ('views', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название фильтра')),
                ('name_slug', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.ManyToManyField(blank=True, related_name='filters', to='item.Category', verbose_name='Для категорий')),
            ],
            options={
                'verbose_name': 'Фильтр',
                'verbose_name_plural': 'Фильтры',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_optional', models.BooleanField(db_index=True, default=False, verbose_name='Это дополнительный товар?')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название ')),
                ('name_lower', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('name_slug', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('price', models.IntegerField(db_index=True, default=0, verbose_name='Цена')),
                ('discount', models.IntegerField(blank=True, db_index=True, default=0, verbose_name='Скидка %')),
                ('page_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название страницы')),
                ('page_description', models.TextField(blank=True, null=True, verbose_name='Описание страницы')),
                ('page_keywords', models.TextField(blank=True, null=True, verbose_name='Keywords')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание товара')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('length', models.CharField(blank=True, max_length=15, verbose_name='Длина')),
                ('width', models.CharField(blank=True, max_length=15, verbose_name='Ширина')),
                ('height', models.CharField(blank=True, max_length=15, verbose_name='Высота')),
                ('article', models.CharField(blank=True, max_length=50, null=True, verbose_name='Артикул')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Отображать товар ?')),
                ('is_present', models.BooleanField(db_index=True, default=True, verbose_name='Товар в наличии ?')),
                ('is_new', models.BooleanField(db_index=True, default=False, verbose_name='Товар новинка ?')),
                ('buys', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ManyToManyField(db_index=True, related_name='category', to='item.Category', verbose_name='Состоит в категориях')),
                ('filter', models.ManyToManyField(blank=True, db_index=True, to='item.Filter', verbose_name='Имеет фильтры')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ItemPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название ')),
                ('name_lower', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('name_slug', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, upload_to='item/part/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Элемент букета',
                'verbose_name_plural': 'Элементы букетов',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Промокод (для создания рандомного значения оставить пустым)')),
                ('promo_discount', models.IntegerField(default=0, verbose_name='Скидка на заказ')),
                ('use_counts', models.IntegerField(blank=True, default=1, verbose_name='Кол-во использований')),
                ('is_unlimited', models.BooleanField(default=False, verbose_name='Неограниченное кол-во использований')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен?')),
                ('expiry', models.DateTimeField(default=datetime.datetime(2020, 2, 3, 11, 22, 41, 258355), verbose_name='Срок действия безлимитного кода')),
            ],
            options={
                'verbose_name': 'Промокод',
                'verbose_name_plural': 'Промокоды',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название подкатегории')),
                ('name_slug', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(upload_to='sub_category_img/', verbose_name='Изображение подкатегории')),
                ('page_title', models.CharField(max_length=255, null=True, verbose_name='Название страницы')),
                ('page_description', models.CharField(max_length=255, null=True, verbose_name='Описание страницы')),
                ('page_keywords', models.TextField(null=True, verbose_name='Keywords')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание подкатегории')),
                ('discount', models.IntegerField(blank=True, default=0, verbose_name='Скидка на все товары в подкатегории %')),
                ('views', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='item.Category')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
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
        migrations.CreateModel(
            name='ItemParts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_part_count', models.IntegerField(default=0, verbose_name='Количество')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='item.Item', verbose_name='Букет')),
                ('item_part', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='item.ItemPart', verbose_name='Состав')),
            ],
            options={
                'verbose_name': 'Элемент букета',
                'verbose_name_plural': 'Элементы букетов',
            },
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='item/big_img/', verbose_name='Изображение товара 570x570')),
                ('image_small', models.CharField(blank=True, default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='item.Item', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Изображение для товара',
                'verbose_name_plural': 'Изображения для товара',
            },
        ),
    ]
