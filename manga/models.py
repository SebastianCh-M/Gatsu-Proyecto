from django.db import models

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
    idManga=models.CharField(max_length=30, primary_key=True)
    nombreManga=models.CharField(max_length=50)
    ano_publicacion = models.CharField(max_length=50)
    tsubida=models.ForeignKey(tipoSubida, on_delete=models.CASCADE)
    mangaka=models.CharField(max_length=50)
    sinopsis=models.CharField(max_length=500)
    editorial=models.CharField(max_length=50)
    genero=models.CharField(max_length=50)
    estado=models.ForeignKey(tipoEstado, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='D:\Django Proyectos\Gatsu\static\images')  # configurar la ubicación de almacenamiento según tus necesidades 
    #imagen = MultiImageField()


class SetImagen(models.Model):
    idLote = models.CharField(max_length=255, primary_key=True)
    capitulo= models.CharField(max_length=50) 
    manga = models.ForeignKey(Manga3, on_delete=models.CASCADE)
    grupoImagen = models.ImageField(upload_to='D:\Django Proyectos\Gatsu\static\images')
        


