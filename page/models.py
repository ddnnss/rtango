from django.db import models
from item.models import *

class Banner(models.Model):
    order = models.IntegerField('Порядок отображения', default=1)
    image = models.ImageField('Картинка (1920x680)', upload_to='banners/', blank=False)
    is_active = models.BooleanField(default=True)
    text_top = models.CharField('Заголовок 1', max_length=50, blank=True, null=True)
    text_middle = models.CharField('Заголовок 2', max_length=50, blank=True, null=True)
    text_bottom = models.CharField('Заголовок 3', max_length=50, blank=True, null=True)
    text_button = models.CharField('Надпись на кнопке', max_length=10, blank=True, null=True)
    url = models.CharField('Ссылка с кнопки', max_length=255, blank=True)

    def __str__(self):
        return 'Баннер, порядковый номер : %s' % self.order

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

class OneClick(models.Model):
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Букет')
    phone = models.CharField('Телефон', max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Покупка в 1 клик товара: %s' % self.item.name

    class Meta:
        verbose_name = "Покупка в 1 клик"
        verbose_name_plural = "Покупки в 1 клик"


class Callback(models.Model):
    name = models.CharField('Имя', max_length=20)
    phone = models.CharField('Телефон', max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ обратного звонка. Создан {self.createdAt.date()}'

    class Meta:
        verbose_name = "Заказ обратного звонка"
        verbose_name_plural = "Заказы обратного звонка"