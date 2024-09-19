from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('genre/<int:genre_id>/', views.genre_movies, name='genre_movies'),
    path('trending/', views.trending_movies, name='trending_movies'),
    path('search/', views.proxy_search,  name='search'),
    path('language/<str:language_id>', views.movie_language, name='movie_language'),
]