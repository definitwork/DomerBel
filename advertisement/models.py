from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from django.conf import settings


# Create your models here.

class Advertisement(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Раздел')
    description = models.TextField(verbose_name='Описание')
    bearer = models.CharField(max_length=50, choices=[('Частное лицо', 'Частное лицо'), ('Компания', 'Компания')],
                              verbose_name='Податель')
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Регион, город, район')
    images = models.ForeignKey('Gallery', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Фотографии')
    previous_image = models.ImageField(upload_to='images', default='default/no_image.jpg', verbose_name='Предыдущая фотография')
    contact_name = models.CharField(max_length=255, verbose_name='Контактное лицо')
    phone_num = models.CharField(max_length=255, verbose_name='Телефон')
    email = models.EmailField(verbose_name='E-Mail')
    video_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')  # хранит строку, которая представляет валидный URL-адрес
    moderated = models.BooleanField(default=False, verbose_name='Модерация')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания объявления')
    date_of_deactivate = models.DateTimeField(auto_now=True, verbose_name='Дата деактивации объявления')
    is_active = models.BooleanField(default=False, verbose_name='Активный пользователь?)')
    counter_prosmotr = models.IntegerField(blank=True, null=True, verbose_name='Счетчик просмотров') # над этим еще надо подумать
    slug = models.SlugField(unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Complaint(models.Model):
    reason = models.ForeignKey('ReasonOfComplaint', on_delete=models.CASCADE, verbose_name='Причина жалобы')
    text = models.TextField(verbose_name='Текст жалобы')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания жалобы')
    user = models.CharField(max_length=255, verbose_name='User')
    advertisement = models.ForeignKey('Advertisement', on_delete=models.CASCADE, verbose_name='Объявление')

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

class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Заголовок категории')
    type = models.CharField(max_length=255, choices=[('category_1', 'category_1'), ('category_2', 'category_2'),
                                                     ('category_3', 'category_3'), ('category_4', 'category_4')], verbose_name='Уровень категории')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Отношения')
    slug = models.SlugField(unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self):
        return self.title


class Region(MPTTModel):
    area = models.CharField(max_length=255, verbose_name='Регион, город, район')
    type = models.CharField(max_length=255, choices=[('Область', 'Область'), ('Город', 'Город')], verbose_name='Тип местонахождения')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Отношения')
    slug = models.SlugField(unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
    def __str__(self):
        return self.area


class Gallery(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    photos = models.ManyToManyField('Photo', verbose_name='Связь мм с фотографиями')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.SlugField(unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    photo = models.ImageField(upload_to='images', verbose_name='Фото')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.SlugField(unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return self.name


class Publication(models.Model):
    category = models.CharField(max_length=255, verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Текст с описанием')
    video_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    images = models.ForeignKey('Gallery', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Фотографии')
    date_of_create = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    counter_prosmotr = models.IntegerField(blank=True, null=True, verbose_name='Счетчик просмотров') # над этим еще надо подумать

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(models.Model):
    advertisement = models.ForeignKey('Advertisement', on_delete=models.CASCADE, verbose_name='Связь с объявлением')
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


class FieldSet(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок FieldSet')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Связь с категориями')
    fields = models.ManyToManyField('Field', verbose_name='Связь мм с Fields')

    class Meta:
        verbose_name = 'Набор полей'
        verbose_name_plural = 'Набор полей'

    def __str__(self):
        return self.title


class Field(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок поля')
    spisok_znach = models.ForeignKey('Spisok', on_delete=models.CASCADE, verbose_name='Связь со списком')

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'

    def __str__(self):
        return self.title


class Spisok(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок списка')

    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Списки'

    def __str__(self):
        return self.title


class Element(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок элемента')
    spisok = models.ForeignKey('Spisok', on_delete=models.CASCADE, verbose_name='Связь со списком')

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'

    def __str__(self):
        return self.title


class ElementTwo(models.Model):
    title = models.CharField(max_length=255, verbose_name='Загловок второго элемента')
    element = models.ForeignKey('Element', on_delete=models.CASCADE, verbose_name='Связь с элементом')

    class Meta:
        verbose_name = 'Второй элемент'
        verbose_name_plural = 'Вторые элементы'

    def __str__(self):
        return self.title


class Store(models.Model):
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Связь с регионами')
    title = models.CharField(max_length=255,verbose_name='Название магазина')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    contact_name = models.CharField(max_length=255, verbose_name='Контактное лицо')
    email = models.EmailField(verbose_name='E-Mail')
    phone_num = models.CharField(max_length=255, blank=True, null=True, verbose_name='Номер телефона')
    video_link = models.URLField(blank=True, null=True, verbose_name='Ссылка с видео')  # хранит строку, которая представляет валидный URL-адрес
    logo_image = models.ImageField(upload_to='images', default='default/no_image.jpg', blank=True, null=True, verbose_name='Логотип')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_of_deactivate = models.DateTimeField(auto_now_add=True, verbose_name='Дата деактивации')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='Связь с User')
    is_active = models.BooleanField(default=False, verbose_name='Активный пользователь?)')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Связь с категорией')
    url = models.URLField(blank=True, null=True, verbose_name='Ссылка')  # хранит строку, которая представляет валидный URL-адрес
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')
    counter_prosmotr = models.IntegerField(verbose_name='Счетчик просмотров') # над этим еще надо подумать

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.title