from django.contrib import admin
from django.urls import path
#from .views import MangaListView, MangaCreateView, mangaForm
from . import views
from manga.views import detalle_capitulo, detalle_capitulos, detalle_manga, formManga, libreriaGatsu, verCapitulo
from rest_framework.urlpatterns import format_suffix_patterns



app_name="manga"

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', MangaListView.as_view(), name="Home"),
    #path('create/', MangaCreateView.as_view(), name="create"),
    #path('manga_list/', views.manga_list, name='manga_list'),
    #path('manga_create', formManga),
    path('libreria/', libreriaGatsu, name='libreria_gatsu'),
    path('detalle_manga/<int:manga_id>/', detalle_manga, name='detalle_manga'),
    path('detalle_capitulo/<int:capitulo_id>/', detalle_capitulo, name='detalle_capitulo'),
    path('detalle_capitulos/<int:manga_id>/capitulos/', detalle_capitulos, name='detalle_capitulos'),
    path('verCapitulo/<int:id>', verCapitulo),
]

urlpatterns = format_suffix_patterns(urlpatterns)
