# Generated by Django 5.0 on 2024-01-24 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reasonofcomplaint',
            name='reason',
            field=models.CharField(max_length=1000, verbose_name='Причина жалобы'),
        ),
    ]