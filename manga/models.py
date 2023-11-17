from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from multiselectfield import MultiSelectField

# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=250)
    content=models.TextField()

    def __str__(self):
        return self.title
    
class tipoSubida(models.Model):
    subida=models.CharField(max_length=30)

class tipoEstado(models.Model):
    estado=models.CharField(max_length=30)    

#class Manga2(models.Model):
#    idManga=models.CharField(max_length=30, primary_key=True)
#    nombreManga=models.CharField(max_length=50)
#    ano_publicacion = models.CharField(max_length=50)
#    tsubida=models.ForeignKey(tipoSubida, on_delete=models.CASCADE)
#    mangaka=models.CharField(max_length=50)
#    sinopsis=models.CharField(max_length=500)
#    editorial=models.CharField(max_length=50)
#    genero=models.CharField(max_length=50)
#    estado=models.ForeignKey(tipoEstado, on_delete=models.CASCADE)
    #imagen = models.ImageField(upload_to='portadas/')  # configurar la ubicación de almacenamiento según tus necesidades 
    # 
    # 


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




class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_registro = models.DateField()
    correo = models.EmailField()
    contraseña = models.CharField(max_length=100)

    # Otras informaciones de usuario que necesites

    def __str__(self):
        return self.nombre

class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_registro = models.DateField()
    correo = models.EmailField()
    contraseña = models.CharField(max_length=100)

    # Otras informaciones de administrador que puedan ser necesarias

    def __str__(self):
        return self.nombre

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

    # Otras informaciones del manga que puedan ser relevantes

    def __str__(self):
        return str(self.nombre_manga.nombreManga)

#POST,DELETE,UPDATE
class Capitulo(models.Model):
    titulo = models.CharField(max_length=100)
    numero = models.IntegerField()
    fecha_publicacion = models.DateField()
    manga = models.ForeignKey(MangaGatsu, related_name='capitulos', on_delete=models.CASCADE)

    def __str__(self):
        return str(f"Capítulo {self.numero} - {self.titulo}")

class Imagen(models.Model):
    imagen = models.ImageField(upload_to='manga/capitulos/', storage=FileSystemStorage(location=settings.MEDIA_ROOT))
    capitulo = models.ForeignKey(Capitulo, related_name='imagenes', on_delete=models.CASCADE)

    def __str__(self):
        return self.imagen.url  # O alguna otra representación de la imagen

class RegistroPago(models.Model):
    tipo_usuario = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    # Otras informaciones relacionadas con el registro de pago, si es necesario

    def __str__(self):
        return f"{self.usuario.nombre} - {self.tipo_usuario}"

class Comentario(models.Model):
    contenido = models.TextField()
    fecha_hora = models.DateTimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE)

    # Otras informaciones relacionadas con el comentario, si es necesario

    def __str__(self):
        return f"Comentario de {self.usuario.nombre} en {self.capitulo}"

class Valoracion(models.Model):
    valoracion = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    manga = models.ForeignKey(MangaGatsu, on_delete=models.CASCADE)

    # Otras informaciones relacionadas con la valoración, si es necesario

    def __str__(self):
        return f"Valoración de {self.usuario.nombre} en {self.manga.nombre}"
    







#NO TOMAR EN CUENTA
class Revista2(models.Model):
    editorial_id = models.AutoField(primary_key=True)
    editoriales = models.CharField(max_length=100)

    def __str__(self):
        return self.editoriales


