# Generated by Django 4.2.7 on 2023-11-17 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0016_revista2'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nombremanga',
            unique_together={('revista', 'nombreManga')},
        ),
    ]