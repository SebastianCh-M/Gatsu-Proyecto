from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DeleteView, ListView
from .forms import CustomUserChangeForm, RegisterForm, revistaForm, m_revistaForm, nomMangaForm, m_nomMangaForm, mangaGatsuForm, m_mangaGatsuForm, capituloForm, m_CapituloForm, imagenForm,AddToFavoriteForm ,User
from .models import  HistorialCompras, tipoEstado, tipoSubida, Revista, NombreManga, MangaGatsu, Capitulo, Imagen, Favorite,Progress
from django.views.generic import View, DeleteView
from .forms import ComentarioForm, RegisterForm, revistaForm, m_revistaForm, nomMangaForm, m_nomMangaForm, mangaGatsuForm, m_mangaGatsuForm, capituloForm, m_CapituloForm, imagenForm
from .models import Comentario, HistorialCompras, Valoracion, tipoEstado, tipoSubida, Revista, NombreManga, MangaGatsu, Capitulo, Imagen
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from .models import MangaGatsu
from django.contrib.auth.decorators import login_required
import mercadopago
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout


# Definir una función de prueba para verificar si el usuario pertenece al grupo "Administrador"
def is_admin(user):
    return user.groups.filter(name='Administrador').exists()


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
    
#Metodo POST REVISTA
#def formRevista2(request):
#    if request.method == 'POST':
#        form = revistaForm(request.POST)
#        if form.is_valid():
#            # Si el formulario es valido, se guardan los datos en la tabla
#            form.save()
#            return redirect('/listaRevista')
#    else:
#        form = revistaForm()

#    return render(request, 'formRevista.html',{'form': form})    

@user_passes_test(is_admin)
#METODO GET REVISTA
#def listaRevista(request):  
#    editoriales = Revista.objects.all()
#    datos ={'editoriales': editoriales}
#    return render(request, 'listaRevista.html', datos)  

@user_passes_test(is_admin)
#Metodo DELETE REVISTA    
def deleR(request, id):
    dele = Revista.objects.get(id=id)
    dele.delete()
    return redirect('/formRevista')   

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
#METODO GET nombreManga
#def listaNombreManga(request):  
#    nombres = NombreManga.objects.all()
#    datos ={'nombres': nombres}
#    return render(request, 'listaNombreManga.html', datos)


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

            # Redirige a la vista de detalle después de procesar el formulario
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
    })

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


@user_passes_test(is_admin)
#Metodo POST Capitulo
def formCapitulo(request):
    capitulos = Capitulo.objects.all()
    if request.method == 'POST':
        form = capituloForm(request.POST)
        if form.is_valid():
            # Si el formulario es valido, se guardan los datos en la tabla
            form.save()
            return redirect('/formCapitulo')
    else:
        form = capituloForm()

    return render(request, 'formCapitulo.html',{'form': form,  'capitulos': capitulos})

@user_passes_test(is_admin)
#METODO GET Capitulo
#def listaCapitulo(request):  
#    capitulos = Capitulo.objects.all()
#    datos ={'capitulos': capitulos}
#    return render(request, 'listaCapitulo.html', datos)

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
def formImagen(request):
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
    


def mangaFavorito(request, id):
    manga = get_object_or_404(MangaGatsu, id=id)
    if manga.favorito.filter(id=request.user.id).exists():
        manga.favorito.remove(request.user)
    else:
        manga.favorito.add(request.user)
    return redirect('/Home')        


#def favorite_manga(request):
#    user_favorites = MangaGatsu.objects.filter(favorito=request.user)
#    return render(request, 'favoritos.html', {'user_favorites': user_favorites})


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
    return render(request, 'listaMangaGatsu.html', context)



@login_required
def add_favorite(request, manga_id):
    manga = get_object_or_404(MangaGatsu, id=manga_id)
    user = request.user

    # Check if the manga is already in the user's favorites
    if not Favorite.objects.filter(user=user, manga=manga).exists():
        favorite = Favorite(user=user, manga=manga)
        favorite.save()

    return redirect('manga:detalle_capitulos', manga_id=manga_id)  



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


#def verManga(request):
#    mangas = MangaGatsu.objects.all()

#    if request.method == 'GET':
#        form = filtroManga(request.GET)
#        if form.is_valid() and form.cleaned_data['genero']:
#            mangas = mangas.filter(genre__in=form.cleaned_data['genero'])

#    return render(request, 'verManga.html', {'mangas': mangas, 'form': form})


#def guardarManga(request):
 #def   v_idManga=request.POST.get('idManga')
  #def  v_nombreM=request.POST.get('nombreManga')
   #def v_anoP=request.POST.get('ano_publicacion')
  #def  v_subida=request.POST.get('tsubida')
  #def  v_mangaka=request.POST.get('mangaka')
   #def v_sinopsis=request.POST.get('sinopsis')
   #def v_editorial=request.POST.get('editorial')
   #def v_genero=request.POST.get('genero')
  #def  v_estado=request.POST.get('estado')
#def

  #def  tEstados=tipoEstado.objects.get(estado=v_estado)
   #def tSubidas=tipoSubida.objects.get(subida=v_subida)

   #def nuevo=Manga2()
   #def nuevo.idManga=v_idManga
  #def  nuevo.nombreManga=v_nombreM
   #def nuevo.ano_publicacion=v_anoP
   #def nuevo.tsubida=tSubidas
  #def nuevo.mangaka=v_mangaka
   #def nuevo.sinopsis=v_sinopsis
   #def nuevo.editorial=v_editorial
   #def nuevo.genero=v_genero
    #defnuevo.estado=tEstados
   #def 

    #defManga2.save(nuevo)

    #defreturn render(request, 'loginC.html')    



    nuevo=Manga2()
    nuevo.idManga=v_idManga
    nuevo.nombreManga=v_nombreM
    nuevo.ano_publicacion=v_anoP
    nuevo.tsubida=tSubidas
    nuevo.mangaka=v_mangaka
    nuevo.sinopsis=v_sinopsis
    nuevo.editorial=v_editorial
    nuevo.genero=v_genero
    nuevo.estado=tEstados
    

    Manga2.save(nuevo)

    return render(request, 'loginC.html')    

#vista para gestionar subscripcion

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
            # Otros datos necesarios para la suscripción
            # Ejemplo: 
             "auto_recurring": {
                 "frequency": 1,
                 "frequency_type": "months",
                 "transaction_amount": 4000.00,
                 "currency": "CLP",}
        }

        try:
            # Realizar la solicitud de creación de la suscripción a Mercado Pago
            response = mercadopago.post("/preapproval", subscription_data)

            if response["status"] == 201:  # Verificar si la suscripción fue creada exitosamente
                monto = 4000.00  # Definir el monto de la suscripción (esto puede variar según tu lógica)
                
                # Crear un registro en HistorialCompras
                HistorialCompras.objects.create(
                    usuario=request.user,
                    monto=monto,
                )

                return redirect('página_de_confirmación_de_suscripción')
            else:
                # Manejar el caso si la suscripción no se creó correctamente
                # Puedes mostrar un mensaje de error o redirigir a otra página
                error_message = "La suscripción no se creó correctamente."
                # Aquí puedes enviar un mensaje de error o redirigir a una página de error
                # return render(request, 'error.html', {'error_message': error_message})

        except Exception as e:
            # Manejar excepciones en caso de errores durante la solicitud a Mercado Pago
            error_message = f"Error al procesar la suscripción: {str(e)}"
            # Aquí puedes registrar los detalles del error en algún registro o mostrar un mensaje de error al usuario
            # return render(request, 'error.html', {'error_message': error_message})

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