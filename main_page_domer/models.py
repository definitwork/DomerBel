import calendar
from datetime import datetime, timedelta

from django.db import models

from django.conf import settings

from advertisement.models import Region, Category, Advertisement


# Create your models here.
class Store(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион')
    title = models.CharField(max_length=60,verbose_name='Название магазина')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    contact_name = models.CharField(max_length=100, verbose_name='Контактное лицо')
    email = models.EmailField(verbose_name='E-Mail')
    phone_num = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    video_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на YouTube видео')  # хранит строку, которая представляет валидный URL-адрес
    logo_image = models.ImageField(upload_to='images/store_img', default='default/no_image.jpg', blank=True, null=True, verbose_name='Логотип')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_of_deactivate = models.DateTimeField(blank=True, null=True, verbose_name='Дата деактивации')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Пользователь, создавший магазин')
    is_active = models.BooleanField(default=False, verbose_name='Активный магазин')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    url = models.URLField(blank=True, null=True, verbose_name='Ссылка на сайт магазина')  # хранит строку, которая представляет валидный URL-адрес
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')
    counter_views = models.IntegerField(default=0, verbose_name='Счетчик просмотров')

    def save(self, *args, **kwargs):
        day_now = datetime.now()
        if calendar.isleap(int(day_now.strftime('%Y'))) and int(day_now.strftime("%m")) <= 2:
            self.date_of_deactivate = day_now + timedelta(days=366)
        else:
            self.date_of_deactivate = day_now + timedelta(days=365)
        super(Store, self).save(*args, **kwargs)


    def get_days_till_expiration(self):
        days_till_expiration = self.date_of_deactivate - self.date_of_create
        return days_till_expiration.days

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.title


class Comment(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Связь с объявлением')
    comment = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, verbose_name='Автор')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    moderated = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.author


class Complaint(models.Model):
    reason = models.ForeignKey('ReasonOfComplaint', on_delete=models.CASCADE, verbose_name='Причина жалобы')
    text = models.TextField(verbose_name='Текст жалобы')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания жалобы')
    user = models.CharField(max_length=255, verbose_name='User')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление')

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'

    def __str__(self):
        return self.reason.reason


class ReasonOfComplaint(models.Model):
    reason = models.CharField('Причина жалобы', max_length=1000)

    class Meta:
        verbose_name = 'Причина жалобы'
        verbose_name_plural = 'Причины жалобы'

    def __str__(self):
        return self.reason


class PhotoPublication(models.Model):
    photo = models.ImageField(upload_to='images', verbose_name='Фото')
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, verbose_name='Публикация')

    class Meta:
        verbose_name = 'Фото публикации'
        verbose_name_plural = 'Фото публикаций'

    def __str__(self):
        return self.publication


class Publication(models.Model):
    category = models.CharField(max_length=255, verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Текст с описанием')
    video_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    preview_image = models.ImageField(upload_to='images',
                                      verbose_name='Главная фотография')
    date_of_create = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    counter_views = models.IntegerField(default=0, verbose_name='Счетчик просмотров')
    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title