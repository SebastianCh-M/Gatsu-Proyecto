# Generated by Django 4.2.7 on 2023-12-02 22:45

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0022_auto_20231202_1936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='capitulo',
        ),
        migrations.AddField(
            model_name='comentario',
            name='manga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manga.mangagatsu'),
        ),
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
