from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comentario, Revista, NombreManga, MangaGatsu, Capitulo, Imagen
from multiupload.fields import MultiFileField


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class revistaForm(forms.ModelForm):
    class Meta:
        model = Revista
        fields = ['editoriales']

class m_revistaForm(forms.ModelForm):
    class Meta:
        model = Revista
        fields = ['editoriales']   



class nomMangaForm(forms.ModelForm):
    class Meta:
        model = NombreManga
        fields = ['revista','nombreManga','mangaka'] 

class m_nomMangaForm(forms.ModelForm):
    class Meta:
        model = NombreManga
        fields = ['revista', 'nombreManga', 'mangaka']



class mangaGatsuForm(forms.ModelForm):
    class Meta:
        model = MangaGatsu
        fields = ['nombre_manga', 'anio_publicacion', 'tipo_subida', 'sinopsis', 'genero', 'estado', 'portada']

class m_mangaGatsuForm(forms.ModelForm):
    class Meta:
        model = MangaGatsu
        fields = ['nombre_manga', 'anio_publicacion', 'tipo_subida', 'sinopsis', 'genero', 'estado', 'portada']    



class capituloForm(forms.ModelForm):
    class Meta:
        model = Capitulo
        fields = ['titulo', 'numero', 'fecha_publicacion', 'manga']

class m_CapituloForm(forms.ModelForm):
    class Meta:
        model = Capitulo
        fields = ['titulo', 'numero', 'fecha_publicacion', 'manga']        



class imagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['imagen', 'capitulo']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["contenido", "manga"]
        widgets = {'manga': forms.HiddenInput()}
        





#class PostCreateForm(forms.ModelForm):
#    class Meta:
#        model=Post
#        fields=('title', 'content')

#class mangaForm(forms.ModelForm):
#    class Meta:
#        model = Manga3
#        fields = ['idManga', 'nombreManga', 'ano_publicacion','tsubida','mangaka','sinopsis','editorial','genero','estado','imagen'] 

       


#class imagenForm(forms.ModelForm):
#    class Meta:
#        model = SetImagen    
#        fields = ['idLote', 'capitulo', 'manga','grupoImagen']

        



#class imagenForm2(forms.ModelForm):     
#        idLote = forms.CharField(max_length=255)
#        capitulo = forms.CharField(max_length=255)
#        manga = forms.ModelChoiceField(queryset=Manga3.objects.all())       
#        grupoImagen = MultiFileField(min_num=1, max_num=10)