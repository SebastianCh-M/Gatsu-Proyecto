from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DeleteView
from .forms import revistaForm, m_revistaForm, nomMangaForm, m_nomMangaForm, mangaGatsuForm, m_mangaGatsuForm, capituloForm, m_CapituloForm, imagenForm
from .models import HistorialCompras, tipoEstado, tipoSubida, Revista, NombreManga, MangaGatsu, Capitulo, Imagen
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from .models import MangaGatsu
from django.contrib.auth.decorators import login_required
import mercadopago

# Create your views here.


class MangaListView(View):
    def get(self, request, *args, **kwargs):
        context={
            
        }
        return render(request, 'manga_list.html', context )
    
#Metodo POST REVISTA
def formRevista(request):
    if request.method == 'POST':
        form = revistaForm(request.POST)
        if form.is_valid():
            # Si el formulario es valido, se guardan los datos en la tabla
            form.save()
            return redirect('/listaRevista')
    else:
        form = revistaForm()

    return render(request, 'formRevista.html',{'form': form})    

#METODO GET REVISTA
def listaRevista(request):  
    editoriales = Revista.objects.all()
    datos ={'editoriales': editoriales}
    return render(request, 'listaRevista.html', datos)  

#Metodo DELETE REVISTA    
def deleR(request, id):
    dele = Revista.objects.get(id=id)
    dele.delete()
    return redirect('/listaRevista')   

#METODO UPDATE REVISTA 
def updaR(request, id):
    data = Revista.objects.get(id=id)
    form = m_revistaForm(instance=data)

    if request.method == 'POST':
        form = m_revistaForm(request.POST, instance= data)
        if form.is_valid():
            form.save()
        return redirect('/listaRevista')    

    context = {'form': form}
    return render(request, 'modRevista.html', context)  


#Metodo POST nombreManga
def formNombreManga(request):
    if request.method == 'POST':
        form = nomMangaForm(request.POST)
        if form.is_valid():
            # Si el formulario es valido, se guardan los datos en la tabla
            form.save()
            return redirect('/listaNombreManga')
    else:
        form = nomMangaForm()

    return render(request, 'formNombreManga.html',{'form': form})

#METODO GET nombreManga
def listaNombreManga(request):  
    nombres = NombreManga.objects.all()
    datos ={'nombres': nombres}
    return render(request, 'listaNombreManga.html', datos)


#Metodo DELETE nombreManga    
def deleN(request, id):
    dele = NombreManga.objects.get(id=id)
    dele.delete()
    return redirect('/listaNombreManga')   

#METODO UPDATE nombreManga 
def updaN(request, id):
    data = NombreManga.objects.get(id=id)
    form = m_nomMangaForm(instance=data)

    if request.method == 'POST':
        form = m_nomMangaForm(request.POST, instance= data)
        if form.is_valid():
            form.save()
        return redirect('/listaNombreManga')    

    context = {'form': form}
    return render(request, 'modNombreManga.html', context)



#Metodo POST MangaGatsu
def formMangaGatsu(request):
    if request.method == 'POST':
        form = mangaGatsuForm(request.POST, request.FILES)
        if form.is_valid():
            # Si el formulario es valido, se guardan los datos en la tabla
            form.save()
            return redirect('/listaMangaGatsu')
    else:
        form = mangaGatsuForm()

    return render(request, 'formMangaGatsu.html',{'form': form})

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
    
    return render(request, 'verCapitulo.html', {'capitulos': capitulo, 'imagenes': imagen})

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
    try:
        manga = MangaGatsu.objects.get(pk=manga_id)
        capitulos = Capitulo.objects.filter(manga=manga)
    except MangaGatsu.DoesNotExist:
        raise Http404("Manga no encontrado.")

    return render(request, 'detalle_capitulo.html', {'manga': manga, 'capitulos': capitulos})


#Metodo DELETE nombreManga    
def deleM(request, id):
    dele = MangaGatsu.objects.get(id=id)
    dele.delete()
    return redirect('/listaMangaGatsu')   

#METODO UPDATE nombreManga 
def updaM(request, id):
    data = MangaGatsu.objects.get(id=id)
    form = m_mangaGatsuForm(instance=data)

    if request.method == 'POST':
        form = m_mangaGatsuForm(request.POST, request.FILES ,instance= data)
        if form.is_valid():
            form.save()
        return redirect('/listaMangaGatsu')    

    context = {'form': form}
    return render(request, 'modNombreManga.html', context)



#Metodo POST Capitulo
def formCapitulo(request):
    if request.method == 'POST':
        form = capituloForm(request.POST)
        if form.is_valid():
            # Si el formulario es valido, se guardan los datos en la tabla
            form.save()
            return redirect('/listaCapitulo')
    else:
        form = capituloForm()

    return render(request, 'formCapitulo.html',{'form': form})


#METODO GET Capitulo
def listaCapitulo(request):  
    capitulos = Capitulo.objects.all()
    datos ={'capitulos': capitulos}
    return render(request, 'listaCapitulo.html', datos)

#Metodo DELETE Capitulo    
def deleC(request, id):
    dele = Capitulo.objects.get(id=id)
    dele.delete()
    return redirect('/listaCapitulo')   

#METODO UPDATE Capitulo 
def updaC(request, id):
    data = Capitulo.objects.get(id=id)
    form = m_CapituloForm(instance=data)

    if request.method == 'POST':
        form = m_CapituloForm(request.POST, instance= data)
        if form.is_valid():
            form.save()
        return redirect('/listaCapitulo')    

    context = {'form': form}
    return render(request, 'modCapitulo.html', context)


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
    

#Metodo GET Imagen
def listaImagen(request):  
    imagenes = Imagen.objects.all()
    datos ={'imagenes': imagenes}
    return render(request, 'listaImagen.html', datos)


#Metodo DELETE Imagen    
def deleI(request, id):
    dele = Imagen.objects.get(id=id)
    dele.delete()
    return redirect('/listaImagen')   

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

def formManga(request):
    tEstado=tipoEstado.objects.all()
    tSubida=tipoSubida.objects.all()
    datos = {'tipoEstados':tEstado,'tipoSubidas': tSubida}

    return render(request, 'registrarM.html', datos)


#def guardarManga(request):
    v_idManga=request.POST.get('idManga')
    v_nombreM=request.POST.get('nombreManga')
    v_anoP=request.POST.get('ano_publicacion')
    v_subida=request.POST.get('tsubida')
    v_mangaka=request.POST.get('mangaka')
    v_sinopsis=request.POST.get('sinopsis')
    v_editorial=request.POST.get('editorial')
    v_genero=request.POST.get('genero')
    v_estado=request.POST.get('estado')


    tEstados=tipoEstado.objects.get(estado=v_estado)
    tSubidas=tipoSubida.objects.get(subida=v_subida)

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
