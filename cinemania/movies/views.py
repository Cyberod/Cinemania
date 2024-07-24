from django.shortcuts import render
from django.conf import settings
import requests
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator


# Create your views here.

api_base_url = settings.TMDB_API_BASE_URL
image_base_url = settings.TMDB_IMAGE_BASE_URL
api_key = settings.TMDB_API_KEY

def fetch_from_tmdb(endpoint, params=None):
    url = f"{api_base_url}/{endpoint}"
    if not params:
        params = {}
    params['api_key'] = api_key
    response = requests.get(url, params=params)
    return response.json()


def home(request):

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
    # https://developers.themoviedb.org/3/movies/get-movie-details
    movie_detail_url = api_base_url + "movie/" + str(movie_id) + "?"
    movie_casts_url = api_base_url + "movie/" + str(movie_id) + "/casts?"
    trailers_url = api_base_url + "movie/" + str(movie_id) + "/videos?"

    params = {
    "api_key": api_key,
    "language": "en-US",
    "casts": "casts",
    }

    movie = requests.get(movie_detail_url, params=params).json()
    movie_casts = requests.get(movie_casts_url, params=params).json().get("cast", [] )[:4]
    movie_crew = requests.get(movie_casts_url, params=params).json().get("crew", [] )
    trailers_data = requests.get(trailers_url, params=params).json().get("results", [])

    context = { 
        "movie": movie, "image_base_url": image_base_url,
        "movie_casts": movie_casts,
        "movie_crew": movie_crew,
        "trailers": trailers_data
        }

    return render(request,'movies/movie_detail.html', context)



def search_movies(request):
    query = request.GET.get('query')
    params = {
        "api_key": api_key,
        "language": "en-US",
        "query": query,
    }
    
    if query:
        response = requests.get(api_base_url + "search/movie", params=params)
        if response.status_code == 200:
            data = response.json()
            movies = data.get('results', [])
            data = response.json()
    
    context = { 
        'movies': movies, 
        'image_base_url': image_base_url, 
        'query': query 
        }

    return render(request, 'movies/search_movies.html', context)

def genre_movies(request, genre_id):

    # TMDB endpoint for genres
    genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US'

    # Get the list of genres to find the specific genre
    response = requests.get(genre_url)
    genres = response.json().get('genres', [])
    genre = next((g for g in genres if g['id'] == genre_id), None) # next: returns the first match or none if there is no matchafter iteration
    
    if not genre:
        # Handle the case where the genre is not found
        return render(request, '404.html', status=404)
    
    # TMDB endpoint for movies in the specified genre
    movies_url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}&year=2024&sort_by=popularity.desc'
    
    # Get the list of movies in the specified genre
    movies_data = requests.get(movies_url).json()
    movies = movies_data.get('results', [])
   

    # Create context with genre and movies
    context = {
        'image_base_url': image_base_url,
        'genre': genre,
        'movies': movies,
    }
    
    # Render the 'genre_movies.html' template with the context data
    return render(request, 'movies/genre_movies.html', context)


# 1:45pm
