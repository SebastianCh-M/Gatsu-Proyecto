from django.contrib import admin
from django.urls import path
#from .views import MangaListView, MangaCreateView, mangaForm
from . import views
from manga.views import detalle_capitulo, detalle_capitulos, detalle_manga, formManga, libreriaGatsu, perfil_usuario, procesar_formulario, verCapitulo, mangaFavorito,add_to_favorite, AddToFavoriteView, listaFavoritos, manga_list, add_favorite, update_progress,score_selection
from manga.views import detalle_capitulo, detalle_capitulos, detalle_manga, formManga, libreriaGatsu, procesar_formulario, verCapitulo, mangaFavorito,add_to_favorite, AddToFavoriteView, listaFavoritos, manga_list, add_favorite, update_progress,deleF
from manga.views import detalle_capitulo, detalle_capitulos, detalle_manga, formManga, libreriaGatsu, perfil_usuario, procesar_formulario, verCapitulo, mangaFavorito,add_to_favorite, AddToFavoriteView, listaFavoritos, manga_list, add_favorite, update_progress
from manga.views import detalle_capitulo, detalle_capitulos, detalle_manga, formManga, libreriaGatsu, procesar_formulario, verCapitulo, mangaFavorito,add_to_favorite, AddToFavoriteView, listaFavoritos, manga_list, add_favorite, update_progress,deleF, marcar_leido
from rest_framework.urlpatterns import format_suffix_patterns


app_name="manga"

urlpatterns = [
    #Login y Registrar
    path('sign-up', views.sign_up, name='sign_up'),
    #path('', MangaListView.as_view(), name="Home"),
    #path('create/', MangaCreateView.as_view(), name="create"),
    #path('manga_list/', views.manga_list, name='manga_list'),
    #path('manga_create', formManga),
    path('libreria/', libreriaGatsu, name='libreria_gatsu'),
    path('detalle_manga/<int:manga_id>/', detalle_manga, name='detalle_manga'),
    path('detalle_capitulo/<int:capitulo_id>/', detalle_capitulo, name='detalle_capitulo'),
    path('detalle_capitulos/<int:manga_id>/capitulos/', detalle_capitulos, name='detalle_capitulos'),
    path('procesar_formulario/<int:manga_id>/', procesar_formulario, name='procesar_formulario'),
    path('mangaFavorito/<int:id>', mangaFavorito, name='mangaFavorito'),
    path('verCapitulo/<int:id>', verCapitulo),
    #path('favoritos/', favorite_manga, name='favorite_manga'), 
    #path('favorite_manga/', FavoriteMangaListView.as_view(), name='favorite_manga'), 
    path('add_to_favorite/', AddToFavoriteView.as_view(), name='add_to_favorite'),
    #path('favorite_manga/', favorite_manga, name='favorite_manga'),
    #path('favorite_manga/', FavoriteComicsView.as_view(), name='favorite_manga'),
    path('listaFavoritos', listaFavoritos, name='listaFavoritos'),
    path('manga_list', manga_list),
    #path('add_favorite/', add_favorite, name='add_favorite'),
    path('add_favorite/<int:manga_id>/', add_favorite, name='add_favorite'),
    path('update_progress/<int:manga_id>/<int:chapter_id>/', update_progress, name='update_progress'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('deleF/<int:id>', deleF, name='deleF'),
    path('manga/<int:manga_id>/score/', score_selection, name='score_selection'),
    path('marcar_leido/<int:capitulo_id>/', marcar_leido, name='marcar_leido'),
]

urlpatterns = format_suffix_patterns(urlpatterns)