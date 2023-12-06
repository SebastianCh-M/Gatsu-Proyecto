from django.contrib import admin
from .models import tipoEstado, tipoSubida, Manga3, MangaGatsu, Capitulo, Imagen, Comentario, Valoracion, Revista, NombreManga, Revista2, Favorite,Progress
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User



class ImagenInLine(admin.TabularInline):
    model = Imagen

class subidaAdmin(admin.ModelAdmin):
    list_display = ["subida"]

class estadoAdmin(admin.ModelAdmin):
    list_display = ["estado"]

class editorialAdmin(admin.ModelAdmin):
    list_display = ["editorial_id","editoriales"] 

class favoriteAdmin(admin.ModelAdmin):
    list_display = ["id","user","manga"]      

class progressAdmin(admin.ModelAdmin):
    list_display = ["id","user","manga", "last_read_chapter"]    

    

admin.site.register(Revista2, editorialAdmin)    
admin.site.register(tipoSubida, subidaAdmin)
admin.site.register(tipoEstado, estadoAdmin)     
admin.site.register(Manga3)
admin.site.register(Revista)  # Registrar la tabla Revista

admin.site.register(Favorite, favoriteAdmin)
admin.site.register(Progress, progressAdmin)



@admin.register(MangaGatsu)
class MangaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_manga', 'anio_publicacion', 'tipo_subida', 'get_revista', 'genero', 'estado', 'portada')
    list_filter = ('estado', 'genero')

    def get_revista(self, obj):
        return obj.nombre_manga.revista.editoriales

    get_revista.short_description = 'Revista'

@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    list_display = ('id', 'capitulo', 'show_image')

    def show_image(self, obj):
        return mark_safe(f'<img src="{obj.imagen.url}" style="max-height:100px;max-width:100px;" />')

    show_image.allow_tags = True
    show_image.short_description = 'Imagen'

@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'numero', 'fecha_publicacion', 'manga')
    inlines = [ImagenInLine]

    def __str__(self):
        return f"CapÃ­tulo {self.numero} - {self.titulo}"


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'contenido', 'fecha_creado', 'fecha_modificado', 'manga')

@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('id', 'valoracion', 'usuario', 'manga')

@admin.register(NombreManga)
class NombreMangaAdmin(admin.ModelAdmin):
    list_display = ('id', 'revista', 'nombreManga', 'mangaka')