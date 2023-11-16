from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import mangaForm, PostCreateForm
from .models import tipoEstado, tipoSubida, Manga3


# Create your views here.

class MangaListView(View):
    def get(self, request, *args, **kwargs):
        context={
            
        }
        return render(request, 'manga_list.html', context )
    
#class MangaCreateView(View):
#    def get(self, request,*args, **kwargs):
#        context={
#            
#        }
#        return render(request, 'manga_create.html', context)
#    
#    def post(self, request,*args, **kwargs):
#        context={
            
#        }
#        return render(request, 'manga_create.html', context)
    
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



def registrarManga(request):
    if request.method == 'POST':
        form = mangaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manga_list')
    else:
        form = mangaForm()
    return render(request, 'manga_create.html', {'form': form})

def manga_list(request):
    Man = Manga3.objects.all()
    return render(request, 'manga_list.html', {'mangas': Man})