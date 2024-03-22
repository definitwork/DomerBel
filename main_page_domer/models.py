from django.db import models
from django.conf import settings
from advertisement.models import Advertisement


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