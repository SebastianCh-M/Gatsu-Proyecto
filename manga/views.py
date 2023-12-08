from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from .forms import CustomUserChangeForm, RegisterForm, revistaForm, m_revistaForm, nomMangaForm, m_nomMangaForm, mangaGatsuForm, m_mangaGatsuForm, capituloForm, m_CapituloForm, imagenForm,AddToFavoriteForm
from .models import  HistorialCompras, tipoEstado, tipoSubida, Revista, NombreManga, MangaGatsu, Capitulo, Imagen, Favorite,Progress
from django.views.generic import View
from .forms import ComentarioForm, RegisterForm, revistaForm, m_revistaForm, nomMangaForm, m_nomMangaForm, mangaGatsuForm, m_mangaGatsuForm, capituloForm, m_CapituloForm, imagenForm, ScoreForm
from .models import Comentario, HistorialCompras, Valoracion, tipoEstado, tipoSubida, Revista, NombreManga, MangaGatsu, Capitulo, Imagen, Score
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import MangaGatsu
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Avg

# Definir una función de prueba para verificar si el usuario pertenece al grupo "Administrador"
def is_admin(user):
    return user.groups.filter(name='Administrador').exists()


#Metodo Score
def score_selection(request, manga_id):
    manga = MangaGatsu.objects.get(id=manga_id)
    user = request.user

    # Check if the user has already scored this manga
    existing_score = Score.objects.filter(user=user, manga=manga).first()

    if existing_score:
        if request.method == 'POST':
            form = ScoreForm(request.POST, instance=existing_score)
            if form.is_valid():
                form.save()
                return redirect('manga:detalle_capitulos', manga_id=manga_id)
        else:
            form = ScoreForm(instance=existing_score)

    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score_value = form.cleaned_data['score_value']
            Score.objects.create(user=user, manga=manga, score_value=score_value)
            return redirect('manga:detalle_capitulos', manga_id=manga_id)
    else:
        form = ScoreForm()

    return render(request, 'score_selection.html', {'form': form, 'manga': manga})

#Vista para Sign-up (Registrarse)
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user =  form.save()
            login(request, user)
            return redirect('Home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

class MangaListView(View):
    def get(self, request, *args, **kwargs):
        context={
            
        }
        return render(request, 'manga_list.html', context )
    
#Metodo POST y GET REVISTA
@user_passes_test(is_admin)
#Metodo POST REVISTA
def formRevista(request):
    editoriales = Revista.objects.all()
    if request.method == 'POST':
        form = revistaForm(request.POST)
        if form.is_valid():
            # Si el formulario es valido, se guardan los datos en la tabla
            form.save()
            return redirect('/formRevista')
    else:
        form = revistaForm()

    return render(request, 'formRevista.html',{'form': form, 'editoriales': editoriales})    
    
@user_passes_test(is_admin)
#Metodo DELETE REVISTA    
def deleR(request, id):
    dele = Revista.objects.get(id=id)
    dele.delete()
    return redirect('/formRevista')   

@login_required
#Metodo DELETE Favorito    
def deleF(request, id):
    dele = Favorite.objects.get(id=id)
    dele.delete()
    return redirect('/LibreriaGatsu')   

class LibreriaGatsuView(View):
    def get(self, request, *args, **kwargs):
        # Obtener la lista de mangas
        mangas = MangaGatsu.objects.all()

        # Ordenar la lista de mangas por el título alfabéticamente
        mangas = sorted(mangas, key=lambda manga: manga.nombre_manga.nombreManga)

        context = {'mangas': mangas}
        return render(request, 'LibreriaGatsu.html', context)
@user_passes_test(is_admin)
#METODO UPDATE REVISTA 
def updaR(request, id):
    data = Revista.objects.get(id=id)
    form = m_revistaForm(instance=data)

    if request.method == 'POST':
        form = m_revistaForm(request.POST, instance= data)
        if form.is_valid():
            form.save()
        return redirect('/formRevista')    

    context = {'form': form}
    return render(request, 'modRevista.html', context)  


#Metodo POST Y Get nombreManga
@user_passes_test(is_admin)
#Metodo POST nombreManga
def formNombreManga(request):
    nombres = NombreManga.objects.all()
    if request.method == 'POST':
        form = nomMangaForm(request.POST)
        if form.is_valid():
            # Si el formulario es valido, se guardan los datos en la tabla
            form.save()
            return redirect('/formNombreManga')
    else:
        form = nomMangaForm()

    return render(request, 'formNombreManga.html',{'form': form, 'nombres': nombres})
@user_passes_test(is_admin)
#Metodo DELETE nombreManga    
def deleN(request, id):
    dele = NombreManga.objects.get(id=id)
    dele.delete()
    return redirect('/formNombreManga')   

@user_passes_test(is_admin)
#METODO UPDATE nombreManga 
def updaN(request, id):
    data = NombreManga.objects.get(id=id)
    form = m_nomMangaForm(instance=data)

    if request.method == 'POST':
        form = m_nomMangaForm(request.POST, instance= data)
        if form.is_valid():
            form.save()
        return redirect('/formNombreManga')    

    context = {'form': form}
    return render(request, 'modNombreManga.html', context)



#Metodo POST Y GET MangaGatsu
@user_passes_test(is_admin)
#Metodo POST MangaGatsu
def formMangaGatsu(request):
    mangas = MangaGatsu.objects.all()
    if request.method == 'POST':
        form = mangaGatsuForm(request.POST, request.FILES)
        if form.is_valid():
            # Si el formulario es valido, se guardan los datos en la tabla
            form.save()
            return redirect('/formMangaGatsu')
    else:
        form = mangaGatsuForm()

    return render(request, 'formMangaGatsu.html',{'form': form, 'mangas': mangas})

#METODO GET MangaGatsu
def listaMangaGatsu(request):  
    mangas = MangaGatsu.objects.all()
    datos ={'mangas': mangas}
    return render(request, 'listaMangaGatsu.html', datos)


#METODO GET Para Libreria Gatsu
# Asegúrate de que tu vista envía los géneros disponibles a la plantilla
def libreriaGatsu(request):
    mangas = MangaGatsu.objects.all()
    genres = MangaGatsu.OPCIONES_GENERO
    paginator = Paginator(mangas, 10)
    page = request.GET.get('page')
    editoriales = Revista.objects.all()
    Estado = MangaGatsu.OPCIONES_ESTADO

    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1

    try:
        mangas = paginator.page(page)
    except PageNotAnInteger:
        mangas = paginator.page(1)
    except EmptyPage:
        mangas = paginator.page(paginator.num_pages)
        context = {'mangas': mangas, 'genres': genres}
        return render(request, 'libreriaGatsu.html', context)
    context = {'mangas': mangas, 'genres': genres}
    

    return render(request, 'LibreriaGatsu.html', {'mangas': mangas, 'genres': genres, 'editoriales': editoriales, 'Estado': Estado})


#METODO GET Para ver todos los capitulos por manga
def verCapitulo(request, id):
    capitulo = Capitulo.objects.get(id=id)
    imagen = capitulo.imagenes.all()

    # Verifica si el usuario pertenece al grupo "UsuarioRegistrado" y "UsuarioSuscrito"
    usuario_registrado = request.user.groups.filter(name='UsuarioRegistrado').exists()
    usuario_suscrito = request.user.groups.filter(name='UsuarioSuscrito').exists()

    # Verifica si es el primer capítulo
    primer_capitulo = capitulo.numero == 1

    # Pasa el estado de suscripción del usuario al contexto
    user_is_subscribed = usuario_suscrito

    # Si pertenece al grupo "UsuarioRegistrado" y no es el primer capítulo, muestra un mensaje de advertencia
    if usuario_registrado and not primer_capitulo:
        return render(request, 'verCapitulo.html', {'capitulos': capitulo, 'imagenes': imagen, 'advertencia': True, 'user_is_subscribed': user_is_subscribed})

    # Si todo está bien, muestra el capítulo
    return render(request, 'verCapitulo.html', {'capitulos': capitulo, 'imagenes': imagen, 'advertencia': False, 'user_is_subscribed': user_is_subscribed})


def detalle_manga(request, manga_id):
    manga = get_object_or_404(MangaGatsu, id=manga_id)
    capitulos = Capitulo.objects.filter(manga=manga)

    # Asegurémonos de obtener solo el primer capítulo para este ejemplo
    primer_capitulo = capitulos.first() if capitulos else None

    return render(request, 'detalle_manga.html', {'manga': manga, 'capitulo': primer_capitulo})

#METODO GET Para poder leer el capitulo por manga.
@login_required
def detalle_capitulo(request, capitulo_id):
    capitulo = get_object_or_404(Capitulo, id=capitulo_id)
    imagenes = capitulo.imagenes.all()  # Utiliza el related_name 'imagenes' para obtener todas las imágenes del capítulo

    return render(request, 'detalle_capitulo.html', {'capitulo': capitulo, 'imagenes': imagenes})

@login_required
def detalle_capitulos(request, manga_id):
    manga = get_object_or_404(MangaGatsu, pk=manga_id)
    capitulos = Capitulo.objects.filter(manga=manga)
    
    # Retrieve all scores for the manga
    scores = Score.objects.filter(manga=manga)

    # Calculate the average score using Django's Avg aggregate function
    average_score = scores.aggregate(Avg('score_value'))['score_value__avg']

    user_is_subscribed = request.user.is_authenticated and request.user.groups.filter(name='UsuarioSuscrito').exists()

    comentarios = Comentario.objects.filter(manga=manga)
    rating_actual = Valoracion.objects.filter(usuario=request.user, manga=manga).first()

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.manga = manga
            comentario.save()
            form = ComentarioForm()

            rating = request.POST.get('rating')
            if rating:
                rating = float(rating)
                valoracion_existente = Valoracion.objects.filter(usuario=request.user, manga=manga).first()
                if valoracion_existente:
                    valoracion_existente.valoracion = rating
                    valoracion_existente.save()
                else:
                    Valoracion.objects.create(valoracion=rating, usuario=request.user, manga=manga)

            # Redirige a la vista de detalle despuÃ©s de procesar el formulario
            return redirect(reverse('manga:detalle_capitulos', args=[manga_id]))

    else:
        form = ComentarioForm()

    return render(request, 'detalle_capitulo.html', {
        'manga': manga,
        'capitulos': capitulos,
        'user_is_subscribed': user_is_subscribed,
        'form': form,
        'comentarios': comentarios,
        'rating_actual': rating_actual.valoracion if rating_actual else None,
        'average_score': average_score
    })

@login_required
def marcar_leido(request, capitulo_id):
    # Obtener el capítulo
    capitulo = get_object_or_404(Capitulo, id=capitulo_id)

    # Marcar el capítulo como leído para el usuario actual
    request.user.profile.capitulos_leidos.add(capitulo)

    return JsonResponse({'success': True})

def procesar_formulario(request, manga_id):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.manga = get_object_or_404(MangaGatsu, pk=manga_id)
            comentario.save()
            form = ComentarioForm()

            rating = request.POST.get('rating')
            if rating:
                rating = float(rating)
                valoracion_existente = Valoracion.objects.filter(usuario=request.user, manga=comentario.manga).first()
                if valoracion_existente:
                    valoracion_existente.valoracion = rating
                    valoracion_existente.save()
                else:
                    Valoracion.objects.create(valoracion=rating, usuario=request.user, manga=comentario.manga)

            # Redirige a la vista de detalle después de procesar el formulario
            return redirect(reverse('detalle_capitulos', args=[manga_id]))

    # Manejo adicional si el formulario no es válido o si la solicitud no es POST
    return redirect(reverse('detalle_capitulos', args=[manga_id]))


#Metodo DELETE MangaGatsu    
@user_passes_test(is_admin)
#Metodo DELETE nombreManga    
def deleM(request, id):
    dele = MangaGatsu.objects.get(id=id)
    dele.delete()
    return redirect('/formMangaGatsu')   

#METODO UPDATE MangaGatsu 
@user_passes_test(is_admin)
#METODO UPDATE nombreManga 
def updaM(request, id):
    data = MangaGatsu.objects.get(id=id)
    form = m_mangaGatsuForm(instance=data)

    if request.method == 'POST':
        form = m_mangaGatsuForm(request.POST, request.FILES ,instance= data)
        if form.is_valid():
            form.save()
        return redirect('/formMangaGatsu')    

    context = {'form': form}
    return render(request, 'modNombreManga.html', context)


import requests

@user_passes_test(is_admin)
#Metodo POST Capitulo
def formCapitulo(request):
    capitulos = Capitulo.objects.all()
    if request.method == 'POST':
        form = capituloForm(request.POST)
        if form.is_valid():
            # Guardar el capítulo en la base de datos
            capitulo = form.save()

            # Construir el mensaje para Discord
            mensaje_discord = f'\n-----------------------------------------------\n¡Nuevo capítulo publicado!\n**Manga: {capitulo.manga}**\n**Capítulo {capitulo.numero}:** {capitulo.titulo}\n** Ya disponible en la página Web**\n Enlace: **https://13.51.144.170:8000/LibreriaGatsu **\n-----------------------------------------------\n '

            # URL del Webhook de Discord
            url_webhook = 'https://discord.com/api/webhooks/1182047314274160740/mClrr9Cq1ihAmq8P9SQooewhHoSw7j4NbysgPy_sCGHba1IJdDXQYBps-5hxVE-Ox4YW'

            # Envía el mensaje al servidor de Discord
            response = requests.post(url_webhook, json={'content': mensaje_discord})

            if response.status_code == 204:
                # Éxito al enviar el mensaje
                print('Mensaje enviado con éxito a Discord!')
            else:
                # Manejar cualquier error
                print('Error al enviar el mensaje a Discord:', response.status_code)

            return redirect('/formCapitulo')

    else:
        form = capituloForm()

    return render(request, 'formCapitulo.html', {'form': form, 'capitulos': capitulos})

@user_passes_test(is_admin)
#Metodo DELETE Capitulo    
def deleC(request, id):
    dele = Capitulo.objects.get(id=id)
    dele.delete()
    return redirect('/formCapitulo')   

@user_passes_test(is_admin)
#METODO UPDATE Capitulo 
def updaC(request, id):
    data = Capitulo.objects.get(id=id)
    form = m_CapituloForm(instance=data)

    if request.method == 'POST':
        form = m_CapituloForm(request.POST, instance= data)
        if form.is_valid():
            form.save()
        return redirect('/formCapitulo')    

    context = {'form': form}
    return render(request, 'modCapitulo.html', context)

@user_passes_test(is_admin)
#Metodo POST Imagen
def formImagen(request, manga_id):
    if request.method == 'POST':
        v_imagen = request.FILES.getlist('imagen')
        v_capitulo = request.POST.get('capitulo')
        capitulo = Capitulo.objects.get(id=v_capitulo)

        for imagen in v_imagen:
            nuevo = Imagen(imagen=imagen)
            nuevo.capitulo = capitulo
            nuevo.save()

        return redirect('/listaImagen')
    else:
        # Render the form page
        capitulos = Capitulo.objects.filter(manga__id=manga_id)
        capitulos_con_info = [
            {
                'id': capitulo.id,
                'numero': capitulo.numero,
                'info_completa': f"{capitulo.manga.nombre_manga.nombreManga} - Capítulo {capitulo.numero} - {capitulo.titulo}"
            }
            for capitulo in capitulos
        ]


        
        return render(request, 'formImagen.html', {'capitulos': capitulos_con_info, })


def formImagen3(request):
    if request.method == 'POST':
        v_imagen = request.FILES.getlist('imagen')
        v_capitulo = request.POST.get('capitulo')  
        capitulo = Capitulo.objects.get(id=v_capitulo)

        for imagen in v_imagen:
            nuevo = Imagen(imagen=imagen)
            nuevo.capitulo = capitulo
            nuevo.save()

        return redirect('/listaImagen')
    else:
        # Render the form page
        capitulos = Capitulo.objects.all()
        capitulos_con_info = [
            {
                'id': capitulo.id,
                'numero': capitulo.numero,
                'info_completa': f"{capitulo.manga.nombre_manga.nombreManga} - Capítulo {capitulo.numero} - {capitulo.titulo}"
            }
            for capitulo in capitulos
        ]
        return render(request, 'formImagen.html', {'capitulos': capitulos_con_info})
    

def getManga(request):  
    mangas = MangaGatsu.objects.all()
    datos ={'mangas': mangas}
    return render(request, 'getManga.html', datos)
    
    


def mangaFavorito(request, id):
    manga = get_object_or_404(MangaGatsu, id=id)
    if manga.favorito.filter(id=request.user.id).exists():
        manga.favorito.remove(request.user)
    else:
        manga.favorito.add(request.user)
    return redirect('/Home')        

class FavoriteMangaListView(LoginRequiredMixin, ListView):
    model = MangaGatsu
    template_name = 'favorite_manga.html'
    context_object_name = 'user_favorites'

    def get_queryset(self):
        return MangaGatsu.objects.filter(favorito=self.request.user)
    

def add_to_favorite(request):
    if request.method == 'POST':
        form = AddToFavoriteForm(request.POST)
        if form.is_valid():
            manga_id = form.cleaned_data['manga_id']
            manga = MangaGatsu.objects.get(pk=manga_id)
            Favorite.objects.create(user=request.user, manga=manga)
            return redirect('add_to_favorite')  # Change 'comics_list' to your comics list view name
    else:
         return render(request, 'add_to_favorite.html')    
    

class ComicsListView(View):
    template_name = 'listaMangaGatsu.html'

    def get(self, request, *args, **kwargs):
        manga = MangaGatsu.objects.all()
        form = AddToFavoriteForm()
        return render(request, self.template_name, {'mangas': manga, 'form': form})

class AddToFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = AddToFavoriteForm(request.POST)
        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = request.user
            favorite.save()
        return redirect('/listaMangaGatsu')

class FavoriteComicsView(LoginRequiredMixin, View):
    template_name = 'favorite_manga.html'

    def get(self, request, *args, **kwargs):
        favorite = Favorite.objects.all()
        user_favorites = Favorite.objects.filter(user=request.user)
        return render(request, self.template_name, {'favorites': favorite})  
    


def manga_list(request):
    mangas = MangaGatsu.objects.all()
    user = request.user  # Get the logged-in user

    context = {
        'mangas': mangas,
        'user': user,
    }
    return render(request, 'MiBiblioteca.html', context)



@login_required
def add_favorite(request, manga_id):
    manga = get_object_or_404(MangaGatsu, id=manga_id)
    user = request.user

    # Check if the manga is already in the user's favorites
    if not Favorite.objects.filter(user=user, manga=manga).exists():
        favorite = Favorite(user=user, manga=manga)
        favorite.save()

    return redirect('manga:listaFavoritos')  



@login_required
def listaFavoritos(request):  
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    datos ={'favorites': favorites}
    return render(request, 'MiBiblioteca.html', datos)   


@login_required
def update_progress(request, manga_id, chapter_id):
    manga = MangaGatsu.objects.get(id=manga_id)
    chapter = Capitulo.objects.get(id=chapter_id)

    
    # Update or create progress for the user and manga
    progress, created = Progress.objects.get_or_create(user=request.user, manga=manga)
    progress.last_read_chapter = chapter
    progress.save()

    return redirect('manga:detalle_capitulos', manga_id=manga_id)

#Backup   
def formImagen2(request, m_id):
    manga = MangaGatsu.objects.get(id=m_id)
    v_capitulos = manga.capitulos.all()

    if request.method == 'POST':
        v_imagen = request.FILES.getlist('imagen')
        v_capitulo = request.POST.get('capitulo')  
        capitulo = Capitulo.objects.get(id=v_capitulo)

        for imagen in v_imagen:
            nuevo = Imagen(imagen=imagen)
            nuevo.capitulo = capitulo
            nuevo.save()

        return redirect('/listaImagen')
    else:
        # Render the form page
        capitulos = Capitulo.objects.all()
        capitulos_con_info = [
            {
                'id': capitulo.id,
                'numero': capitulo.numero,
                'info_completa': f"{capitulo.manga.nombre_manga.nombreManga} - Capítulo {capitulo.numero} - {capitulo.titulo}"
            }
            for capitulo in capitulos
        ]
        return render(request, 'formImagen.html', {'capitulos': capitulos_con_info, 'mangas': manga, 'capitulos': v_capitulos}) 


#Metodo GET Imagen
def listaImagen(request):  
    imagenes = Imagen.objects.all()
    datos ={'imagenes': imagenes}
    return render(request, 'listaImagen.html', datos)

@user_passes_test(is_admin)
#Metodo DELETE Imagen    
def deleI(request, id):
    dele = Imagen.objects.get(id=id)
    dele.delete()
    return redirect('/listaImagen')   

@user_passes_test(is_admin)
#METODO UPDATE Imagen 
def updaI(request, id):
    data = Imagen.objects.get(id=id)
    form = imagenForm(instance=data)

    if request.method == 'POST':
        form = imagenForm(request.POST, request.FILES ,instance= data)
        if form.is_valid():
            form.save()
        return redirect('/listaImagen')    

    context = {'form': form}
    return render(request, 'modImagen.html', context)


#METODO ver Imagen
def verCapitulo(request, id):
    capitulo = Capitulo.objects.get(id=id)
    imagen = capitulo.imagenes.all()
    
    return render(request, 'verCapitulo.html', {'capitulos': capitulo, 'imagenes': imagen})

#Metodo ver Capitulo
def verManga(request, id):
    manga = MangaGatsu.objects.get(id=id)
    capitulo = manga.capitulos.all()

    return render(request, 'verManga.html', {'mangas': manga, 'capitulos': capitulo}) 


def formManga(request):
    tEstado=tipoEstado.objects.all()
    tSubida=tipoSubida.objects.all()
    datos = {'tipoEstados':tEstado,'tipoSubidas': tSubida}

    return render(request, 'registrarM.html', datos)
def suscribirse(request):
    if request.method == 'POST':

        # Crear instancia del SDK de Mercado Pago
        mercadopago = mercadopago()
        mercadopago.client_id = 7720091870954518
        mercadopago.client_secret = 'Rk06ELc1XzVZeihc0NXer8PGkxBbJao4'
        # Datos de la suscripción
        subscription_data = {
            "payer_email": request.user.email,
            "back_url": "Home.html",

             "auto_recurring": {
                 "frequency": 1,
                 "frequency_type": "months",
                 "transaction_amount": 4000.00,
                 "currency": "CLP",}
        }

        try:

            response = mercadopago.post("/preapproval", subscription_data)

            if response["status"] == 201: 
                monto = 4000.00 

                HistorialCompras.objects.create(
                    usuario=request.user,
                    monto=monto,
                )

                return redirect('página_de_confirmación_de_suscripción')
            else:

                error_message = "La suscripción no se creó correctamente."


        except Exception as e:

            error_message = f"Error al procesar la suscripción: {str(e)}"


    return render(request, 'pago.html')


def add_favorite2(request):
    if request.method == 'POST':
        user = request.user
        manga_id = request.POST.get('manga_id')
        manga = MangaGatsu.objects.get(id=manga_id)

        # Check if the manga is not already in favorites to avoid duplicates
        if not Favorite.objects.filter(user=user, manga=manga).exists():
            Favorite.objects.create(user=user, manga=manga)

    return redirect('comics_list')  # Redirect back to the comics list after adding to favorites

@login_required
def perfil_usuario(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario')  # Redirige al perfil después de guardar cambios
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'perfil_usuario.html', {'form': form})
@login_required
def guardar_cambios(request):
    if request.method == 'POST':
        form = perfil_usuario(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario') # Redirige a la vista del perfil
    else:
        form = perfil_usuario(instance=request.user)
    return render(request, 'perfil_usuario.html', {'form': form})

