# Generated by Django 4.2.6 on 2023-11-14 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0015_alter_imagen_imagen_alter_manga3_imagen_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revista2',
            fields=[
                ('editorial_id', models.AutoField(primary_key=True, serialize=False)),
                ('editoriales', models.CharField(max_length=100)),
            ],
        ),
    ]
