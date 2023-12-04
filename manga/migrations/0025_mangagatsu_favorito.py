# Generated by Django 4.2.6 on 2023-11-30 20:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manga', '0024_rename_manga_favorito_perfilusuario_manga'),
    ]

    operations = [
        migrations.AddField(
            model_name='mangagatsu',
            name='favorito',
            field=models.ManyToManyField(blank=True, related_name='favorito', to=settings.AUTH_USER_MODEL),
        ),
    ]
