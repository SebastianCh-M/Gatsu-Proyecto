from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from manga.views import formRevista, deleR, updaR, formNombreManga, deleN, updaN, formMangaGatsu, deleM, updaM, formCapitulo, deleC, updaC, formImagen, listaImagen, deleI, updaI, verCapitulo, listaMangaGatsu, verManga, mangaFavorito, listaFavoritos, getManga
from .views import HomeView, RecientesView, TopMangasView, SobreGatsuView, MiBibliotecaView, ConfigMangas
from manga.views import formRevista, libreriaGatsu, deleR, updaR, formNombreManga, deleN, updaN, formMangaGatsu, listaMangaGatsu, deleM, updaM, formCapitulo, deleC, updaC, formImagen, listaImagen, deleI, updaI, verCapitulo
from .views import HomeView, RecientesView, TopMangasView, SobreGatsuView, MiBibliotecaView, ConfigMangas, pagoView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('manga.urls')),
    path('', include('django.contrib.auth.urls')),
    path('pago/', pagoView.as_view(), name='pago'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name = "Home"),
    path('Home', HomeView.as_view(), name='Home'),
    path('ConfigMangas', ConfigMangas.as_view(), name='ConfigMangas'),
    path('Recientes', RecientesView.as_view(), name='recientes'),
    path('TopMangas', TopMangasView.as_view(), name='TopMangas'),
    path('SobreGatsu', SobreGatsuView.as_view(), name='SobreGatsu'),
    path('MiBiblioteca', MiBibliotecaView.as_view(), name='MiBiblioteca'),
    path('', HomeView.as_view(), name='default'),  # Ruta para la página por defecto

    #Revisa
    path('formRevista',formRevista),
   #path('listaRevista',listaRevista),
    path('deleR/<int:id>', deleR),
    path('updaR/<int:id>', updaR),

    #Nombre Manga
    path('formNombreManga',formNombreManga),
    #path('listaNombreManga',listaNombreManga),
    path('deleN/<int:id>', deleN),
    path('updaN/<int:id>', updaN),

    

    #Manga Gatsu
    path('formMangaGatsu',formMangaGatsu),
    path('listaMangaGatsu',listaMangaGatsu),
    path('deleM/<int:id>', deleM),
    path('updaM/<int:id>', updaM),
    path('getManga', getManga, name='getManga'),

    path('mangaFavorito/<int:id>', mangaFavorito, name='mangaFavorito'),
    

    #Capitulo
    path('formCapitulo',formCapitulo),
    #path('listaCapitulo',listaCapitulo),
    path('deleC/<int:id>', deleC),
    path('updaC/<int:id>', updaC),

    #Imagen
    path('formImagen/<int:manga_id>',formImagen, name='formImagen'),
    #path('cargar_capitulos/', cargar_capitulos, name='cargar_capitulos'),

    path('listaImagen',listaImagen),
    path('deleI/<int:id>', deleI),
    path('updaI/<int:id>', updaI),

    path('verCapitulo/<int:id>', verCapitulo),

    path('verManga/<int:id>', verManga),

    #Libreria Manga
    path('LibreriaGatsu', libreriaGatsu, name='LibreriaGatsu'),

    path('verCapitulo/<int:id>', verCapitulo),
    #path('delete_revista/<int:revista_id>', delete_Revista),
    #path('eliminarR/<int:pk>', eliminarRevista),
    #path('manga_create', registrarManga),
    #path('manga_list', manga_list),
    #path('capitulos_form',registrarImagenes)


] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



