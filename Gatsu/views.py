from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from manga.models import MangaGatsu

class HomeView(View):
    def get(self, request, *args, **kwargs):
        # Obtener los primeros 5 mangas con sus detalles de autor y capítulo
        mangas = MangaGatsu.objects.select_related('nombre_manga').prefetch_related('capitulos').all()[:5]

        for manga in mangas:
            # Obtener el último capítulo asociado a cada manga
            ultimo_capitulo = manga.capitulos.last()
            manga.ultimo_capitulo_numero = ultimo_capitulo.numero if ultimo_capitulo else None

        context = {'mangas': mangas}
        return render(request, 'Home.html', context)


class RecientesView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'recientes.html', context)


class TopMangasView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'TopMangas.html', context)


class SobreGatsuView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'SobreGatsu.html', context)

class MiBibliotecaView(View):
        def get(self, request, *args, **kwargs):
            context = {}
            return render(request, 'MiBiblioteca.html', context)
        
class ConfigMangas(View):
        def get(self, request, *args, **kwargs):
            context = {}
            return render(request, 'ConfigMangas.html', context)

class Filtroprueba(View):
        def get(self, request, *args, **kwargs):
            context = {}
            return render(request, 'Filtroprueba.html', context)
        