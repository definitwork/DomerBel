# Generated by Django 5.0 on 2024-03-22 12:40

import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('advertisement', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='advertisement.category', verbose_name='Отношение'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.category', verbose_name='Раздел'),
        ),
        migrations.AddField(
            model_name='elementtwo',
            name='element',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.element', verbose_name='Связь с элементом'),
        ),
        migrations.AddField(
            model_name='field',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='advertisement.category', verbose_name='Связь с категорией'),
        ),
        migrations.AddField(
            model_name='fieldset',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.category', verbose_name='Связь с категориями'),
        ),
        migrations.AddField(
            model_name='fieldset',
            name='fields',
            field=models.ManyToManyField(to='advertisement.field', verbose_name='Связь мм с Fields'),
        ),
        migrations.AddField(
            model_name='photoadvertisement',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.advertisement', verbose_name='Фотография'),
        ),
        migrations.AddField(
            model_name='region',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='advertisement.region', verbose_name='Отношение'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.region', verbose_name='Регион, город, район'),
        ),
        migrations.AddField(
            model_name='field',
            name='spisok',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='advertisement.spisok', verbose_name='Связь со списком'),
        ),
        migrations.AddField(
            model_name='element',
            name='spisok',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.spisok', verbose_name='Связь со списком'),
        ),
        migrations.AddField(
            model_name='store',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='store',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.region', verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='store',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, создавший магазин'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='advertisement.store', verbose_name='Магазин'),
        ),
    ]