from django.urls import path
from . import views

app_name = 'engine'
urlpatterns = [
    path('index', views.index, name='index'),
    path('search', views.search, name='search'),
    path('info/movies', views.movies_info, name='movies_info'),
    path('info/movie/<int:its_index>', views.movie_info, name='movie_info'),
    path('info/celebrities', views.celebrities_info, name='celebrities_info'),
    path('info/celebrity/<int:its_index>', views.celebrity_info,name='celebrity_info'),

]