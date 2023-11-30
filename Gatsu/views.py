
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from manga.models import MangaGatsu, Manga3
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from manga.models import MangaGatsu, Manga3, Valoracion
from manga.models import Valoracion
from manga.models import HistorialCompras
from django.http import HttpResponse
from django.urls import reverse
import mercadopago
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from mercadopago import SDK
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView

def is_admin(user):
    return user.is_authenticated and user.groups.filter(name='Administrador').exists()

def index(request):
    context = {
        'is_admin': is_admin(request.user)
    }
    return render(request, 'index.html', context)


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

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.groups.filter(name='Administrador').exists() or u.is_superuser), name='dispatch')
class ConfigMangas(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'ConfigMangas.html', context)
    
class pagoView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'pago.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = None

        mp = SDK(access_token='APP_USR-7720091870954518-111620-f24bc7f6bf86befca39f3f6bc7f88a5a-1551574777')  # Initialize the Mercado Pago SDK with your access token
        mp.client_id = '7720091870954518'
        mp.client_secret = 'Rk06ELc1XzVZeihc0NXer8PGkxBbJao4'

        subscription_data = {
            "payer_email": email,
            "back_url": reverse('Home'),  # Adjust the return URL according to your configuration
            "auto_recurring": {
                "frequency": 1,
                "frequency_type": "months",
                "transaction_amount": 4000.00,
                "currency": "CLP",
            }
        }

        try:
            response = mp.post("/preapproval", subscription_data)

            if response["status"] == 201:
                monto = 4000.00

                HistorialCompras.objects.create(
                    usuario=request.user,
                    monto=monto,
                )

                return redirect('página_de_confirmación_de_suscripción')
            else:
                error_message = "La suscripción no se creó correctamente."
                # You can send an error message or redirect to an error page
                # return render(request, 'error.html', {'error_message': error_message})

        except Exception as e:
            error_message = f"Error al procesar la suscripción: {str(e)}"
            # You can log the error details or display an error message to the user
            # return render(request, 'error.html', {'error_message': error_message})

        return render(request, 'pago.html')
