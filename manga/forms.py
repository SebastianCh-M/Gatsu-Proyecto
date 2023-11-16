from django import forms

from .models import Post, Manga3, SetImagen

class PostCreateForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title', 'content')

class mangaForm(forms.ModelForm):
    class Meta:
        model = Manga3
        fields = ['idManga', 'nombreManga', 'ano_publicacion','tsubida','mangaka','sinopsis','editorial','genero','estado','imagen'] 


