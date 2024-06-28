# Generated by Django 4.2.7 on 2023-12-04 01:19

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0032_merge_20231203_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\ramir\\OneDrive\\Escritorio\\Gatsu-Proyecto\\static/images'), upload_to='manga/capitulos/'),
        ),
        migrations.AlterField(
            model_name='manga3',
            name='imagen',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\ramir\\OneDrive\\Escritorio\\Gatsu-Proyecto\\static/images'), upload_to='images'),
        ),
        migrations.AlterField(
            model_name='mangagatsu',
            name='portada',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\ramir\\OneDrive\\Escritorio\\Gatsu-Proyecto\\static/images'), upload_to='manga/portadas/'),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='imagenPerfil',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\ramir\\OneDrive\\Escritorio\\Gatsu-Proyecto\\static/images'), upload_to='perfil/'),
        ),
    ]
