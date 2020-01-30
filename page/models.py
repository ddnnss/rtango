from django.db import models

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
