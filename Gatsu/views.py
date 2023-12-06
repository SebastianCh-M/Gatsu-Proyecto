
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Gatsu import settings
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
from mercadopago import SDK
from requests.exceptions import HTTPError
from django.http import JsonResponse
from django.conf import settings

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
        context = {'public_key': settings.MERCADOPAGO_PUBLIC_KEY}
        return render(request, 'pago.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.user.is_authenticated:
                email = request.user.email
            else:
                email = None

            mp = SDK(
                access_token='APP_USR-7720091870954518-111620-f24bc7f6bf86befca39f3f6bc7f88a5a-1551574777',
                client_id='7720091870954518',
                client_secret='Rk06ELc1XzVZeihc0NXer8PGkxBbJao4'
            )

            subscription_data = {
                "payer_email": email,
                "back_url": reverse('Home'),
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

                    # Llama a payment_callback con el ID de pago
                    payment_id = response.get("response", {}).get("id")
                    self.payment_callback(payment_id)

                    return redirect('nombre_de_tu_página_de_confirmación')

                else:
                    error_message = "La suscripción no se creó correctamente."
                    # Puedes enviar un mensaje de error o redirigir a una página de error
                    # return render(request, 'error.html', {'error_message': error_message})

            except HTTPError as e:
                error_message = f"Error al procesar la suscripción: {str(e)}"
                # Puedes registrar los detalles del error o mostrar un mensaje de error al usuario
                # return render(request, 'error.html', {'error_message': error_message})

        # Si la solicitud no es de tipo POST, regresa a la página de pago
        context = {'public_key': settings.MERCADOPAGO_PUBLIC_KEY}
        return render(request, 'pago.html', context)

    def payment_callback(self, payment_id):
        mp = mercadopago.MP(settings.MERCADOPAGO_ACCESS_TOKEN)
        try:
            payment_info = mp.get_payment(payment_id)
            # Maneja la información del pago y actualiza el estado de la suscripción
            # ...

            print("Pago exitoso:", payment_info)

        except Exception as e:
            # Registra o imprime detalles del error
            print(f"Error en el callback de pago: {str(e)}")


