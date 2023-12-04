from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DeleteView
from .forms import ComentarioForm, RegisterForm, revistaForm, m_revistaForm, nomMangaForm, m_nomMangaForm, mangaGatsuForm, m_mangaGatsuForm, capituloForm, m_CapituloForm, imagenForm
from .models import Comentario, HistorialCompras, Valoracion, tipoEstado, tipoSubida, Revista, NombreManga, MangaGatsu, Capitulo, Imagen
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from .models import MangaGatsu
from django.contrib.auth.decorators import login_required
import mercadopago
from django.http import JsonResponse

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

@user_passes_test(is_admin)
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
def detalle_capitulo(request, capitulo_id):
    capitulo = get_object_or_404(Capitulo, id=capitulo_id)
    imagenes = capitulo.imagenes.all()  # Utiliza el related_name 'imagenes' para obtener todas las imágenes del capítulo

    return render(request, 'detalle_capitulo.html', {'capitulo': capitulo, 'imagenes': imagenes})


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
    mangas = MangaGatsu.objects.all()
    capitulos = Capitulo.objects.none()

    if request.method == 'POST':
        v_imagen = request.FILES.getlist('imagen')
        manga = request.POST.get('manga')
        seleccionar_manga = MangaGatsu.objects.get(id=manga) if manga else None

        #Actualizar queryset
        capitulos = Capitulo.objects.filter(manga=seleccionar_manga)

        for imagen in v_imagen:
            nuevo = Imagen(imagen=imagen)
            nuevo.capitulo = capitulos
            nuevo.save()

        return redirect('/listaImagen')
    else:
        return render(request, 'formImagen.html', {'mangas': mangas, 'capitulos': capitulos})  
    

#Backup    
def formImagen2(request):
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



