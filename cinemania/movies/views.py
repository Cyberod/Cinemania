from django.shortcuts import render
from django.conf import settings
import requests

# Create your views here.

def home(request):
    api_base_url = settings.TMDB_API_BASE_URL
    image_base_url = settings.TMDB_IMAGE_BASE_URL
    api_key = settings.TMDB_API_KEY

    params = {
    "api_key": api_key,
    "language": "en-US",
    "sort_by": "popularity.desc",
    }

    # https://developers.themoviedb.org/3/discover/movie-discover
    popular_movie_url = api_base_url + "movie/popular?"
    now_playing_movie_url = api_base_url + "movie/now_playing?"
    upcoming_movie_url = api_base_url + "movie/upcoming?"
    top_rated_movie_url = api_base_url + "movie/top_rated?"
    trending_movie_url = api_base_url + "trending/movie/week?"
    movie_genres_url = api_base_url + "genre/movie/list?"
    
    popular_movies = requests.get(popular_movie_url, params=params).json().get("results", [])
    now_playing_movies = requests.get(now_playing_movie_url, params=params).json().get("results", [])
    upcoming_movies = requests.get(upcoming_movie_url, params=params).json().get("results", [])
    top_rated_movies = requests.get(top_rated_movie_url, params=params).json().get("results", [])
    trending_movies = requests.get(trending_movie_url, params=params).json().get("results", [])
    movie_genres = requests.get(movie_genres_url, params=params).json().get("genres", [])

    context = { "popular_movies": popular_movies, 
               "image_base_url": image_base_url, 
               "now_playing_movies": now_playing_movies,
               "upcoming_movies": upcoming_movies,
               "top_rated_movies": top_rated_movies,
               "trending_movies": trending_movies,
               "movie_genres": movie_genres
               }



    return render(request, 'movies/index.html', context)

def movie_detail(request, movie_id):
    api_base_url = settings.TMDB_API_BASE_URL
    image_base_url = settings.TMDB_IMAGE_BASE_URL
    api_key = settings.TMDB_API_KEY

    params = {
    "api_key": api_key,
    "language": "en-US",
    "append_to_response": "videos,credits,images,release_dates,casts",
    }

    movie_detail_url = api_base_url + "movie/" + str(movie_id) + "?"
    movie_detail = requests.get(movie_detail_url, params=params).json.get("movie", {})

    context = {
        "movie_detail": movie_detail,
        "image_base_url": image_base_url,
    }

    return render(request, "movies/detail.html", context)