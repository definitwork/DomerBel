# Generated by Django 5.0 on 2024-03-12 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='keywords_description',
            field=models.CharField(max_length=2000, verbose_name='Meta описание'),
        ),
    ]
