from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('genre/<int:genre_id>/', views.genre_movies, name='genre_movies'),
    path('search/', views.search_movies, name='search_movies'),
]