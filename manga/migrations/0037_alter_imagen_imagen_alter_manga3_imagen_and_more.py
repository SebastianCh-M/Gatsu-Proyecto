# Generated by Django 4.2.7 on 2023-12-09 01:37

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0036_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Gatsu-Proyecto\\static/images'), upload_to='manga/capitulos/'),
        ),
        migrations.AlterField(
            model_name='manga3',
            name='imagen',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Gatsu-Proyecto\\static/images'), upload_to='images'),
        ),
        migrations.AlterField(
            model_name='mangagatsu',
            name='portada',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Gatsu-Proyecto\\static/images'), upload_to='manga/portadas/'),
        ),
    ]
