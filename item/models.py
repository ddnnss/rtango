from django.db import models
from django.utils import timezone
from pytils.translit import slugify
from PIL import Image
from django.db.models.signals import post_save
import uuid
from random import choices
import string
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.utils.safestring import mark_safe
#from laskshmi import settings
from rtango import settings

import os


def format_number(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num

class Category(models.Model):
    name = models.CharField('Название категории', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение категории 370x150', upload_to='category_img/', blank=True)
    page_title = models.CharField('Название страницы', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы', max_length=255, blank=True, null=True)
    page_keywords = models.TextField('Keywords', blank=True, null=True)
    short_description = models.TextField('Краткое описание для главной', blank=True,)
    description = RichTextUploadingField('Описание категории', blank=True, null=True)
    show_at_index = models.BooleanField('Показывать на главной?', default=False)
    show_at_main_menu = models.BooleanField('Показывать в главном меню отдельной категорией?', default=False)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = Category.objects.filter(name_slug=slug)
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return 'id :%s , %s ' % (self.id, self.name)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.SET_NULL)
    name = models.CharField('Название подкатегории', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение подкатегории', upload_to='sub_category_img/', blank=False)
    page_title = models.CharField('Название страницы', max_length=255, blank=False, null=True)
    page_description = models.CharField('Описание страницы', max_length=255, blank=False, null=True)
    page_keywords = models.TextField('Keywords', blank=False, null=True)
    description = RichTextUploadingField('Описание подкатегории', blank=True, null=True)
    discount = models.IntegerField('Скидка на все товары в подкатегории %', blank=True, default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = SubCategory.objects.filter(name_slug=slug)
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug

        if self.discount > 0:
            all_items = self.item_set.all()
            for item in all_items:
                item.discount = self.discount
                item.save()

        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return 'id :%s , %s ' % (self.id, self.name)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Filter(models.Model):
    category = models.ManyToManyField(Category, blank=True, verbose_name='Для категорий', related_name='filters')
    name = models.CharField('Название фильтра', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = Filter.objects.filter(name_slug=slug)
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug
        super(Filter, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"


class Item(models.Model):
    is_optional = models.BooleanField('Это дополнительный товар?', default=False, db_index=True)
    category = models.ManyToManyField(Category, blank=False, verbose_name='Состоит в категориях', db_index=True, related_name='category')
    filter = models.ManyToManyField(Filter, blank=True, verbose_name='Имеет фильтры', db_index=True)
    name = models.CharField('Название ', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True,db_index=True)
    price = models.IntegerField('Цена', blank=False, default=0, db_index=True)
    discount = models.IntegerField('Скидка %', blank=True, default=0, db_index=True)
    page_title = models.CharField('Название страницы', max_length=255, blank=True, null=True)
    page_description = models.TextField('Описание страницы',  blank=True, null=True)
    page_keywords = models.TextField('Keywords', blank=True, null=True)
    description = RichTextUploadingField('Описание товара', blank=True, null=True)
    comment = models.TextField('Комментарий', blank=True, null=True)
    length = models.CharField('Длина', max_length=15, blank=True)
    width = models.CharField('Ширина', max_length=15,  blank=True)
    height = models.CharField('Высота',  max_length=15,  blank=True)
    article = models.CharField('Артикул', max_length=50, blank=True, null=True)
    is_active = models.BooleanField('Отображать товар ?', default=True, db_index=True)
    is_present = models.BooleanField('Товар в наличии ?', default=True, db_index=True)
    is_new = models.BooleanField('Товар новинка ?', default=False, db_index=True)
    buys = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = Item.objects.filter(name_slug=slug)
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug
        self.name_lower = self.name.lower()
        super(Item, self).save(*args, **kwargs)



    def getfirstimage(self):
        # url = None
        # for img in self.itemimage_set.all():
        #     if img.is_main:
        url = self.images.first().image_small
        return url

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.getfirstimage():
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.getfirstimage()))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Основная картинка'



    @property
    def discount_value(self):
        if self.discount > 0:
            dis_val = self.price - (self.price * self.discount / 100)
        else:
            dis_val = 0
        return (format_number(dis_val))


    def __str__(self):
       return 'id:%s %s ' % (self.id, self.name)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class ItemPart(models.Model):
    name = models.CharField('Название ', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    image = models.ImageField('Изображение', upload_to='item/part/', blank=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = ItemPart.objects.filter(name_slug=slug)
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
                self.name_slug = slug + slugRandom
            else:
                self.name_slug = slug
        self.name_lower = self.name.lower()
        super(ItemPart, self).save(*args, **kwargs)

    def __str__(self):
       return f'{self.name}'

    class Meta:
        verbose_name = "Элемент букета"
        verbose_name_plural = "Элементы букетов"

class ItemParts(models.Model):
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Букет')
    item_part = models.ForeignKey(ItemPart, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Состав')
    item_part_count = models.IntegerField('Количество', default=0)

    def __str__(self):
       return f'{self.item_part.name} в составе букета {self.item.name}'

    class Meta:
        verbose_name = "Элемент букета"
        verbose_name_plural = "Элементы букетов"

class ItemImage(models.Model):
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Товар', related_name='images')
    image = models.ImageField('Изображение товара 570x570', upload_to='item/big_img/', blank=False)
    image_small = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s Изображение для товара : %s ' % (self.id, self.item.name)

    class Meta:
        verbose_name = "Изображение для товара"
        verbose_name_plural = "Изображения для товара"

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.image_small:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image_small))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Картинка'


    def save(self, *args, **kwargs):
        fill_color = '#fff'
        image = Image.open(self.image).convert('RGB')

        if image.mode in ('RGBA', 'LA'):
            background = Image.new(image.mode[:-1], image.size, fill_color)
            background.paste(image, image.split()[-1])
            image = background
        image.thumbnail((270, 300), Image.ANTIALIAS)
        small_name = 'media/items/{}/{}'.format(self.item.id, str(uuid.uuid4()) + '.jpg')
        # if settings.DEBUG:
        os.makedirs('media/items/{}'.format(self.item.id), exist_ok=True)
        image.save(small_name, 'JPEG', quality=75)
        # else:
        #     os.makedirs('C:/inetpub/wwwroot/khimiya/media/items/{}'.format(self.item.id), exist_ok=True)
        #     image.save('khimiya/' + small_name, 'JPEG', quality=75)
        self.image_small = '/' + small_name

        super(ItemImage, self).save(*args, **kwargs)



class PromoCode(models.Model):
    promo_code = models.CharField('Промокод (для создания рандомного значения оставить пустым)', max_length=255, blank=True, null=True)
    promo_discount = models.IntegerField('Скидка на заказ', blank=False, default=0)
    use_counts = models.IntegerField('Кол-во использований', blank=True, default=1)
    is_unlimited = models.BooleanField('Неограниченное кол-во использований', default=False)
    is_active = models.BooleanField('Активен?', default=True)
    expiry = models.DateTimeField('Срок действия безлимитного кода', default=timezone.now())

    def __str__(self):
        if self.is_unlimited:
            return 'Неограниченный промокод со скидкой : %s . Срок действия до : %s' % (self.promo_discount, self.expiry)
        else:
            return 'Ограниченный промокод со скидкой : %s . Оставшееся кол-во использований : %s' % (self.promo_discount, self.use_counts)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def save(self, *args, **kwargs):
        if self.is_unlimited:
            if not self.promo_code:
                self.promo_code = "LM-"+''.join(choices(string.ascii_uppercase + string.digits, k=5))
                self.use_counts = 0
        else:
            if not self.promo_code:
                self.promo_code = "LM-" + ''.join(choices(string.ascii_uppercase + string.digits, k=5))


        super(PromoCode, self).save(*args, **kwargs)




class Promotion(models.Model):
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Букет')
    topText = models.CharField('Заголовок', max_length=25,null=True,blank=False)
    description = models.TextField('Описание', null=True,blank=False)
    expiry = models.CharField('Окончание акции (в формате год/месяц/день)',max_length=25, null=True, blank=False)

    def __str__(self):
        return f'Акция до {self.expiry} для товара {self.item.name}'

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

#2021/09/01