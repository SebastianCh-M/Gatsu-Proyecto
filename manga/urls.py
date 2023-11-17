from django.contrib import admin
from django.urls import path
from .views import MangaListView, MangaCreateView, mangaForm
from . import views
from manga.views import formManga
from rest_framework.urlpatterns import format_suffix_patterns



app_name="manga"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MangaListView.as_view(), name="home"),
    path('create/', MangaCreateView.as_view(), name="create"),
    path('manga_list/', views.manga_list, name='manga_list'),
    path('manga_create', formManga),
]

urlpatterns = format_suffix_patterns(urlpatterns)
