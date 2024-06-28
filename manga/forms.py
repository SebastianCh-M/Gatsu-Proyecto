from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, Revista, NombreManga, MangaGatsu, Capitulo, Imagen, Favorite, Score
from .models import Comentario, Revista, NombreManga, MangaGatsu, Capitulo, Imagen
from multiupload.fields import MultiFileField
from django.contrib.auth.forms import UserChangeForm


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

class AddToFavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['user','manga']        

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'fecha_nacimiento', 'foto_perfil', 'genero')

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score_value']      
