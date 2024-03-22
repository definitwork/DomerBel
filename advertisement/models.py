import calendar
from datetime import datetime, timedelta

from django.contrib.postgres.fields import ArrayField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from django.conf import settings



class PhotoAdvertisement(models.Model):
    photo = models.ImageField(upload_to='images', verbose_name='Фото')
    advertisement = models.ForeignKey('Advertisement', on_delete=models.CASCADE, verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фото объявления'
        verbose_name_plural = 'Фото объявлений'

    def __str__(self):
        return self.advertisement


class Advertisement(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.CharField(max_length=255, blank=True, null=True, verbose_name="Артикул")
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0, verbose_name='Цена')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Раздел')
    bearer = models.CharField(max_length=50, choices=[('Частное лицо', 'Частное лицо'), ('Компания', 'Компания')],
                              verbose_name='Податель')
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Регион, город, район')
    preview_image = models.ImageField(upload_to='images', default='default/no_image.jpg',
                                      verbose_name='Главная фотография')
    counter_views = models.IntegerField(default=0, verbose_name='Счетчик просмотров')
    contact_name = models.CharField(max_length=255, verbose_name='Контактное лицо')
    phone_num = models.CharField(max_length=255, verbose_name='Телефон')
    email = models.EmailField(verbose_name='E-Mail')
    store = models.ForeignKey('Store', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Магазин")
    slug = models.SlugField(unique=True, verbose_name='URL')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания объявления')
    date_of_deactivate = models.DateTimeField(blank=True, null=True, verbose_name='Дата деактивации объявления')
    moderated = models.BooleanField(default=False, verbose_name='Прошло модерацию')
    is_active = models.BooleanField(default=False, verbose_name='Объявление активно')
    vip = models.BooleanField(default=False, verbose_name="Сделать VIP-объявлением")
    highlight_ad = models.BooleanField(default=False, verbose_name="Выделить объявление")
    special_accommodation = models.BooleanField(default=False, verbose_name="Спецразмещение")
    raise_in_search = models.BooleanField(default=False, verbose_name="Поднять в поиске")
    additional_information = models.JSONField()
    description = models.TextField(verbose_name='Описание')
    video_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')  # хранит строку, которая представляет валидный URL-адрес

    def get_days_till_expiration(self):
        days_till_expiration = self.date_of_deactivate - self.date_of_create
        return days_till_expiration.days

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.date_of_deactivate = datetime.now() + timedelta(days=180)
        super(Advertisement, self).save(*args, **kwargs)


class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Категория')
    type = models.CharField(max_length=255,
                            choices=[('category_1', 'category_1'), ('category_2', 'category_2'),
                                     ('category_3', 'category_3'), ('category_4', 'category_4')],
                            verbose_name='Уровень категории')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Отношение')
    fav_title = models.CharField(max_length=1000, verbose_name="Заголовок на вкладке", blank=True, null=True)
    keywords = models.CharField(max_length=3000, verbose_name="Ключевые слова", blank=True, null=True)
    keywords_description = models.CharField(max_length=3000, verbose_name="Meta описание", blank=True, null=True)
    main_title = models.CharField(max_length=1000, verbose_name="Главный заголовок", blank=True, null=True)
    slug = models.SlugField(unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Region(MPTTModel):
    area = models.CharField(max_length=255, verbose_name='Область, город')
    type = models.CharField(max_length=255, choices=[('Область', 'Область'), ('Город', 'Город')],
                            verbose_name='Тип местонахождения')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Отношение')
    slug = models.SlugField(unique=True, verbose_name='URL')

    class MPTTMeta:
        order_insertion_by = ('area',)

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self):
        return self.area


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
    title = models.CharField(max_length=500, verbose_name='Заголовок поля')
    error = models.CharField(max_length=500, verbose_name='Текст ошибки при неверно введенных данных')
    spisok = models.ForeignKey('Spisok', on_delete=models.CASCADE, verbose_name='Связь со списком', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Связь с категорией', blank=True, null=True)
    int_val_list = ArrayField(models.CharField(max_length=1000, blank=True, null=True, verbose_name='Список числовых значений для задания диапазонов фильтрации'), default=list)
    min_val_interval_date = models.IntegerField(verbose_name='Минимально возможный год для выбора', blank=True, null=True)
    max_val_interval_date = models.IntegerField(verbose_name='Максимально возможный год для выбора', blank=True, null=True)
    search = models.CharField(max_length=500, blank=True, null=True)


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
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Регион')
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
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
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