from django.db import models
from django.db.models.signals import post_save, post_delete
from customuser.models import User, Guest
from item.models import Item, PromoCode
from django.utils.safestring import mark_safe

class Wishlist(models.Model):
    client = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                               verbose_name='Клиент')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Товар')

    def __str__(self):
        return 'Закладка клиента : %s ' % self.client.email

    class Meta:
        verbose_name = "Закладка клиента"
        verbose_name_plural = "Закладки клиентов"


class OrderStatus(models.Model):
    name = models.CharField('Статус для заказа', max_length=100, blank=False)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "Статус для заказа"
        verbose_name_plural = "Статусы для заказов"

class OrderPayment(models.Model):
    name = models.CharField('Вариант оплаты заказа', max_length=100, blank=False)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "Вариант оплаты заказа"
        verbose_name_plural = "Варианты оплаты заказов"

class OrderShipping(models.Model):
    name = models.CharField('Вариант доставки заказа', max_length=100, blank=False)
    price = models.IntegerField('Стоимость доставки', blank=False, null=True)
    isFree = models.BooleanField('Бесплатная доставка при заказе от ', default=False)
    freePrice = models.IntegerField('этой суммы заказа', default=0)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "Вариант доставки заказа"
        verbose_name_plural = "Варианты доставки заказов"

class Order(models.Model):
    receiver_name = models.CharField('ФИО получателя', max_length=100, blank=True, null=True)
    receiver_phone = models.CharField('Телефон получателя', max_length=100, blank=True, null=True)
    sender_name = models.CharField('ФИО отправителя', max_length=100, blank=True, null=True)
    sender_phone = models.CharField('Телефон отправителя', max_length=100, blank=True, null=True)
    sender_email = models.CharField('Email отправителя', max_length=100, blank=True, null=True)
    order_date = models.CharField('Дата доставки', max_length=100, blank=True, null=True)
    order_time = models.CharField('Время доставки', max_length=100, blank=True, null=True)
    is_need_photo = models.BooleanField('Нужно фото при доставке', default=False, null=True)
    card_text = models.TextField('Текст открытки',  blank=True, null=True)
    receiver_address = models.TextField('Адрес доставки',  blank=True, null=True)
    client = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE,
                               verbose_name='Заказ клиента')
    guest = models.ForeignKey(Guest, blank=True, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='Заказ гостя')
    promo_code = models.ForeignKey(PromoCode, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                              verbose_name='Использованный промо-код')
    status = models.ForeignKey(OrderStatus, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                              verbose_name='Статус заказа')
    payment = models.CharField('Оплата', max_length=100, blank=True, null=True)
    shipping = models.ForeignKey(OrderShipping, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                                verbose_name='Доставка заказа')

    total_price = models.IntegerField('Общая стоимость заказа', default=0)
    total_price_with_code = models.DecimalField('Общая стоимость заказа с учетом промо-кода', decimal_places=2,
                                                max_digits=10, default=0)
    order_code = models.CharField('Код заказа', max_length=10, blank=True, null=True)
    is_complete = models.BooleanField('Заказ выполнен ?', default=False)
    is_payd = models.BooleanField('Заказ оплачен ?', default=False)
    sber_orderId = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Заказ № {self.id}. Создан : {self.created_at.strftime("%d-%m-%Y")}  . Сумма заказа :{self.total_price}'
        # if self.client:
        #     if self.promo_code:
        #         return 'Заказ № %s. Создан : %s  . Клиент: %s . Сумма заказа : %s' % (
        #         self.id, self.created_at.strftime('%d-%m-%Y'), self.client.email, self.total_price_with_code)
        #     else:
        #         return 'Заказ № %s. Создан : %s  . Клиент: %s . Сумма заказа : %s' % (
        #         self.id, self.created_at.strftime('%d-%m-%Y'), self.client.email, self.total_price)
        # if self.guest:
        #     if self.promo_code:
        #         return 'Заказ № %s. Создан : %s  . Гость: %s . Сумма заказа : %s' % (
        #         self.id, self.created_at.strftime('%d-%m-%Y'), self.guest.email, self.total_price_with_code)
        #     else:
        #         return 'Заказ № %s. Создан : %s  . Гость: %s . Сумма заказа : %s' % (
        #         self.id, self.created_at.strftime('%d-%m-%Y'), self.guest.email, self.total_price)


    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def created_tag(self):

        return mark_safe('<strong>{}</strong>'.format(self.created_at.strftime('%d-%m-%Y, %H:%M:%S')))

    created_tag.short_description = mark_safe('<strong>Дaта заказа</strong>')

    def save(self, *args, **kwargs):
        if self.promo_code:
            self.total_price_with_code = self.total_price - (self.total_price * self.promo_code.promo_discount / 100)
        else:
            self.total_price_with_code = self.total_price


        super(Order, self).save(*args, **kwargs)





class ItemsInOrder(models.Model):
    order = models.ForeignKey(Order, blank=False, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='В заказе')
    item = models.ForeignKey(Item, blank=True, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='Товар')
    number = models.IntegerField('Кол-во', blank=True, null=True, default=0)
    current_price = models.IntegerField('Цена за ед.', default=0)
    total_price = models.IntegerField('Общая стоимость', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.item.discount > 0:
            self.current_price = self.item.price - (self.item.price * self.item.discount / 100)
        else:
            self.current_price = self.item.price
        self.total_price = self.number * self.current_price

        super(ItemsInOrder, self).save(*args, **kwargs)


    def __str__(self):
        return 'Товар : %s . В заказе № %s .' % (self.item.name, self.order.id)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def getfirstimage(self):
        return self.item.images.first().image_small

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.getfirstimage():
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.getfirstimage()))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    def name_tag(self):
        name = self.item.name
        return name

    def article_tag(self):
        name = self.item.article
        return name

    article_tag.short_description = 'Артикул'
    name_tag.short_description = 'Название товара'
    image_tag.short_description = 'Основная картинка'


def ItemsInOrder_post_save(sender,instance,**kwargs):
    try:
        order = instance.order
    except:
        order = None

    if order:
        order_total_price = 0
        all_items_in_order = ItemsInOrder.objects.filter(order=order)

        for item in all_items_in_order:
            order_total_price += item.total_price

        instance.order.total_price = order_total_price
        instance.order.save(force_update=True)


post_delete.connect(ItemsInOrder_post_save, sender=ItemsInOrder)
post_save.connect(ItemsInOrder_post_save, sender=ItemsInOrder)
