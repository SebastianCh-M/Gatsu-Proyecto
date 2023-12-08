# Generated by Django 4.2.6 on 2023-12-06 02:07

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.files.storage
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('manga', '0033_merge_20231205_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('genero', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('No especificado', 'No especificado')], default='No especificado', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_custom_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_custom_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='D:\\Tesis\\Gatsu-Proyecto\\static/images'), upload_to='manga/capitulos/'),
        ),
        migrations.AlterField(
            model_name='manga3',
            name='imagen',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='D:\\Tesis\\Gatsu-Proyecto\\static/images'), upload_to='images'),
        ),
        migrations.AlterField(
            model_name='mangagatsu',
            name='portada',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='D:\\Tesis\\Gatsu-Proyecto\\static/images'), upload_to='manga/portadas/'),
        ),
        migrations.DeleteModel(
            name='perfilUsuario',
        ),
    ]
