# Generated by Django 5.0 on 2024-02-02 13:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0004_alter_store_counter_prosmotr'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='store',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активный магазин'),
        ),
        migrations.AlterField(
            model_name='store',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.region', verbose_name='Регион'),
        ),
        migrations.AlterField(
            model_name='store',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на сайт магазина'),
        ),
        migrations.AlterField(
            model_name='store',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, создавший магазин'),
        ),
        migrations.AlterField(
            model_name='store',
            name='video_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на YouTube видео'),
        ),
    ]