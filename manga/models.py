from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver
from multiselectfield import MultiSelectField
from datetime import timedelta
from django.db.models import Avg
from django.utils import timezone
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.models import Group


group, created = Group.objects.get_or_create(name='UsuarioSuscrito')


class Post(models.Model):
    title=models.CharField(max_length=250)
    content=models.TextField()

    def __str__(self):
        return self.title
    

    
class tipoSubida(models.Model):
    subida=models.CharField(max_length=30)

class tipoEstado(models.Model):
    estado=models.CharField(max_length=30)    

class Manga3(models.Model):
    idManga = models.CharField(max_length=30, primary_key=True)
    nombreManga = models.CharField(max_length=50)
    ano_publicacion = models.CharField(max_length=50)
    tsubida = models.ForeignKey(tipoSubida, on_delete=models.CASCADE)
    mangaka = models.CharField(max_length=50)
    sinopsis = models.CharField(max_length=500)
    editorial = models.CharField(max_length=50)
    genero = models.CharField(max_length=50)
    estado = models.ForeignKey(tipoEstado, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='images', storage=FileSystemStorage(location=settings.MEDIA_ROOT))


#POST,DELETE,UPDATE    
class Revista(models.Model):
    editoriales = models.CharField(max_length=100)

    def __str__(self):
        return self.editoriales

class NombreManga(models.Model):
    revista = models.ForeignKey(Revista, on_delete=models.CASCADE)
    nombreManga = models.CharField(max_length=100)
    mangaka = models.CharField(max_length=100)

    class Meta:
        unique_together = ['revista', 'nombreManga']

    def __str__(self):
        return f"{self.nombreManga} - {self.revista}"

class MangaGatsu(models.Model):
    nombre_manga = models.ForeignKey(NombreManga, on_delete=models.CASCADE, default=1)
    anio_publicacion = models.DateField()

    OPCIONES_SUBIDA = [
        ('Semanal', 'Semanal'),
        ('Mensual', 'Mensual'),
        ('Otro', 'Otro'),
    ]
    
    tipo_subida = models.CharField(max_length=20, choices=OPCIONES_SUBIDA)
    sinopsis = models.TextField()
    
    OPCIONES_GENERO = [
    ('Accion', 'Acción'),
    ('Aventura', 'Aventura'),
    ('Ciencia Ficcion', 'Ciencia Ficción'),
    ('Comedia', 'Comedia'),
    ('Drama', 'Drama'),
    ('Fantasia', 'Fantasía'),
    ('Harem', 'Harem'),
    ('Horror', 'Terror'),
    ('Mecha', 'Mecha'),
    ]

    genero = MultiSelectField(choices=OPCIONES_GENERO, max_choices=9, max_length=15)

    OPCIONES_ESTADO = [
        ('Publicacion', 'Publicación'),
        ('Finalizado', 'Finalizado'),
        ('Pausado', 'Pausado'),
        ('En Hiato', 'En Hiato'),
        ('En Curso', 'En Curso'),
    ]

    estado = models.CharField(max_length=20, choices=OPCIONES_ESTADO)
    portada = models.ImageField(upload_to='manga/portadas/', storage=FileSystemStorage(location=settings.MEDIA_ROOT))
    favorito = models.ManyToManyField(User, related_name='favorito', blank= True)

    # Otras informaciones del manga que puedan ser relevantes

    def __str__(self):
        return str(self.nombre_manga.nombreManga)
    
    def get_absolute_url(self):
        return reverse('detalle_capitulos', args=[str(self.id)])
    
    @property
    def valoracion_promedio(self):
        return Valoracion.objects.filter(manga=self).aggregate(promedio=Avg('valoracion'))['promedio']
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(MangaGatsu, on_delete=models.CASCADE) 





#POST,DELETE,UPDATE
class Capitulo(models.Model):
    titulo = models.CharField(max_length=100)
    numero = models.IntegerField()
    fecha_publicacion = models.DateField()
    manga = models.ForeignKey(MangaGatsu, related_name='capitulos', on_delete=models.CASCADE)

    def __str__(self):
        return str(f"Capítulo {self.numero} - {self.titulo}")
    
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(MangaGatsu, on_delete=models.CASCADE)
    last_read_chapter = models.ForeignKey(Capitulo, on_delete=models.SET_NULL, null=True)


class Imagen(models.Model):
    imagen = models.ImageField(upload_to='manga/capitulos/', storage=FileSystemStorage(location=settings.MEDIA_ROOT))
    capitulo = models.ForeignKey(Capitulo, related_name='imagenes', on_delete=models.CASCADE)

    def __str__(self):
        return self.imagen.url  # O alguna otra representación de la imagen
    

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creado = models.DateTimeField(default=timezone.now, editable=False)
    fecha_modificado = models.DateTimeField(auto_now=True)
    manga = models.ForeignKey(MangaGatsu, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.manga}"

class Valoracion(models.Model):
    valoracion = models.DecimalField(max_digits=3, decimal_places=1)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(MangaGatsu, on_delete=models.CASCADE, related_name='valoraciones')

    def __str__(self):
        return f"Valoración de {self.usuario.username} en {self.manga.nombre_manga}"

    




class perfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(MangaGatsu, related_name='mangas', on_delete=models.CASCADE) 
    imagenPerfil = models.ImageField(upload_to='perfil/', storage=FileSystemStorage(location=settings.MEDIA_ROOT))


    

#NO TOMAR EN CUENTA
class Revista2(models.Model):
    editorial_id = models.AutoField(primary_key=True)
    editoriales = models.CharField(max_length=100)

    def __str__(self):
        return self.editoriales


class EstadisticasLecturaManga(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(MangaGatsu, on_delete=models.CASCADE)
    total_capitulos_leidos = models.IntegerField(default=0)
    tiempo_total_lectura = models.DurationField(default=timedelta())

class EstadisticasLecturaCapitulo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE)
    tiempo_lectura = models.DurationField(default=timedelta())

class HistorialCompras(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - ${self.monto} - {self.fecha_compra}"

class PreferenciasLectura(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(MangaGatsu, on_delete=models.CASCADE)
    preferencias_lectura = models.TextField(blank=True, null=True)


@receiver(post_save, sender=User)
def asignar_grupo_por_defecto(sender, instance, created, **kwargs):
    if created:
        grupo_usuario_registrado = Group.objects.get(name='UsuarioRegistrado')
        instance.groups.add(grupo_usuario_registrado)
