# Generated by Django 5.0 on 2024-03-12 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Цена')),
                ('bearer', models.CharField(choices=[('Частное лицо', 'Частное лицо'), ('Компания', 'Компания')], max_length=50, verbose_name='Податель')),
                ('preview_image', models.ImageField(default='default/no_image.jpg', upload_to='images', verbose_name='Главная фотография')),
                ('counter_views', models.IntegerField(default=0, verbose_name='Счетчик просмотров')),
                ('contact_name', models.CharField(max_length=255, verbose_name='Контактное лицо')),
                ('phone_num', models.CharField(max_length=255, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='E-Mail')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('date_of_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания объявления')),
                ('date_of_deactivate', models.DateTimeField(blank=True, null=True, verbose_name='Дата деактивации объявления')),
                ('moderated', models.BooleanField(default=False, verbose_name='Прошло модерацию')),
                ('is_active', models.BooleanField(default=False, verbose_name='Объявление активно')),
                ('vip', models.BooleanField(default=False, verbose_name='Сделать VIP-объявлением')),
                ('highlight_ad', models.BooleanField(default=False, verbose_name='Выделить объявление')),
                ('special_accommodation', models.BooleanField(default=False, verbose_name='Спецразмещение')),
                ('raise_in_search', models.BooleanField(default=False, verbose_name='Поднять в поиске')),
                ('additional_information', models.JSONField()),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Категория')),
                ('type', models.CharField(choices=[('category_1', 'category_1'), ('category_2', 'category_2'), ('category_3', 'category_3'), ('category_4', 'category_4')], max_length=255, verbose_name='Уровень категории')),
                ('fav_title', models.CharField(max_length=1000, verbose_name='Заголовок на вкладке')),
                ('keywords', models.CharField(max_length=1000, verbose_name='Ключевые слова')),
                ('keywords_description', models.CharField(max_length=1000, verbose_name='Meta описание')),
                ('main_title', models.CharField(max_length=1000, verbose_name='Главный заголовок')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок элемента')),
            ],
            options={
                'verbose_name': 'Элемент',
                'verbose_name_plural': 'Элементы',
            },
        ),
        migrations.CreateModel(
            name='ElementTwo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Загловок второго элемента')),
            ],
            options={
                'verbose_name': 'Второй элемент',
                'verbose_name_plural': 'Вторые элементы',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок поля')),
            ],
            options={
                'verbose_name': 'Поле',
                'verbose_name_plural': 'Поля',
            },
        ),
        migrations.CreateModel(
            name='FieldSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок FieldSet')),
            ],
            options={
                'verbose_name': 'Набор полей',
                'verbose_name_plural': 'Набор полей',
            },
        ),
        migrations.CreateModel(
            name='PhotoAdvertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='images', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Фото объявления',
                'verbose_name_plural': 'Фото объявлений',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=255, verbose_name='Область, город')),
                ('type', models.CharField(choices=[('Область', 'Область'), ('Город', 'Город')], max_length=255, verbose_name='Тип местонахождения')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.CreateModel(
            name='Spisok',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок списка')),
            ],
            options={
                'verbose_name': 'Список',
                'verbose_name_plural': 'Списки',
            },
        ),
    ]
