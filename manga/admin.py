from django.contrib import admin
from .models import tipoEstado, tipoSubida, Manga3

# Register your models here.

class subidaAdmin(admin.ModelAdmin):
    list_display=["subida"]

class estadoAdmin(admin.ModelAdmin):
    list_display=["estado"]

class mangaAdmin(admin.ModelAdmin):
    list_display=['idManga', 'nombreManga', 'ano_publicacion','tsubida','mangaka','sinopsis','editorial','genero','estado','imagen']    




#-------------Registro----------------------

admin.site.register(tipoSubida, subidaAdmin)
admin.site.register(tipoEstado, estadoAdmin)     
admin.site.register(Manga3, mangaAdmin)