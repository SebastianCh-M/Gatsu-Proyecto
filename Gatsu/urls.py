from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from manga.views import registrarManga, manga_list
from .views import HomeView, RecientesView, TopMangasView, SobreGatsuView, MiBibliotecaView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name = "home"),
    path('Home', HomeView.as_view(), name='home'),
    path('Recientes.html', RecientesView.as_view(), name='recientes'),
    path('TopMangas.html', TopMangasView.as_view(), name='TopMangas'),
    path('SobreGatsu.html', SobreGatsuView.as_view(), name='SobreGatsu'),
    path('MiBiblioteca.html', MiBibliotecaView.as_view(), name='MiBiblioteca'),
    path('Home.html', HomeView.as_view(), name='home'),  # Ruta para la página por defecto
    path('manga_create.html', registrarManga),
    path('manga_list.html', manga_list),
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


