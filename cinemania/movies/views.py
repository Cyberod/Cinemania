from django.shortcuts import render
from django.conf import settings
import requests
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
import json



# Create your views here.

api_base_url = settings.TMDB_API_BASE_URL
image_base_url = settings.TMDB_IMAGE_BASE_URL
api_key = settings.TMDB_API_KEY

DESIRED_LANGUAGES = [
                        'Igbo',
                        'Yoruba',
                        'Hausa',
]

def fetch_from_tmdb(endpoint, params=None):
    url = f"{api_base_url}/{endpoint}"
    if not params:
        params = {}
    params['api_key'] = api_key
    response = requests.get(url, params=params)
    return response.json()

import requests
from django.conf import settings

def global_context(request):
    
    params = {
        "api_key": api_key,
    }
    
    # Fetch movie genres
    movie_genres_url = api_base_url + "genre/movie/list?"
    movie_genres = requests.get(movie_genres_url, params=params).json().get("genres", [])
    
    # Fetch languages
    languages_url = api_base_url + "configuration/languages?"
    languages = requests.get(languages_url, params=params).json()
    


    return {
        'movie_genres': movie_genres,
        'languages': languages,
        'nig_language': DESIRED_LANGUAGES,
    }





def home(request):

    params = {
    "api_key": api_key,
    "sort_by": "popularity.desc",
    }

    # https://developers.themoviedb.org/3/discover/movie-discover
    popular_movie_url = api_base_url + "movie/popular?"
    now_playing_movie_url = api_base_url + "movie/now_playing?"
    upcoming_movie_url = api_base_url + "movie/upcoming?"
    top_rated_movie_url = api_base_url + "movie/top_rated?"
    movie_genres_url = api_base_url + "genre/movie/list?"
    languages_url = api_base_url + "configuration/languages?"
    
    
    popular_movies = requests.get(popular_movie_url, params=params).json().get("results", [])
    now_playing_movies = requests.get(now_playing_movie_url, params=params).json().get("results", [])
    upcoming_movies = requests.get(upcoming_movie_url, params=params).json().get("results", [])
    top_rated_movies = requests.get(top_rated_movie_url, params=params).json().get("results", [])
    movie_genres = requests.get(movie_genres_url, params=params).json().get("genres", [])
    languages = requests.get(languages_url, params=params).json()
    #print('languages:', languages)

    genre_dict = {genre['id']: genre['name'] for genre in movie_genres}
    nig_language = DESIRED_LANGUAGES

    #print('LANGUGES:', nig_language)
    #language = next((lang for lang in languages if lang['english_name'] in nig_language), None)
    #print('language:', language)

    context = { 
               "popular_movies": popular_movies, 
               "image_base_url": image_base_url, 
               "now_playing_movies": now_playing_movies,
               "upcoming_movies": upcoming_movies,
               "top_rated_movies": top_rated_movies,
               "movie_genres": movie_genres,
               "nig_language": nig_language,
               "languages": languages,
               "genre_dict": genre_dict,
               }



    return render(request, 'movies/index.html', context)

def trending_movies(request):

    trending_movies = []
    page_number = request.GET.get('page', 1)
    params = {
    "api_key": api_key,
    "language": "en-US",
    "sort_by": "popularity.desc",
    "page": f'{page_number}',
    }
    trending_movies_url = api_base_url + "trending/movie/week?"
    response = requests.get(trending_movies_url, params=params)
    if response.status_code == 200:
        data = response.json()
        trending_movies = data.get('results', [])
        total_pages = data['total_pages']

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = {
                'page': int(page_number),
                'total_pages': total_pages,
                'movie': trending_movies,
                'image_base_url': image_base_url,
                'has_next': int(page_number) < total_pages,
                'next_page':int(page_number) + 1 if int(page_number) < total_pages else None,
            }
            return JsonResponse(context)

        
        context = {
            'movies': trending_movies,
            'image_base_url': image_base_url,
            'has_next': int(page_number) < total_pages,
            'next_page':int(page_number) + 1 if int(page_number) < total_pages else None,
        }
        
        return render(request, 'movies/trending.html', context)
    else:
        # Handling the error gracefully
        context = {
            'error': 'Unable to fetch trending movies at the moment'
        }
        return render(request, 'movies/trending.html', context)

def movie_detail(request, movie_id):
    # https://developers.themoviedb.org/3/movies/get-movie-details
    movie_detail_url = api_base_url + "movie/" + str(movie_id) + "?"
    movie_casts_url = api_base_url + "movie/" + str(movie_id) + "/casts?"
    trailers_url = api_base_url + "movie/" + str(movie_id) + "/videos?"
    recommendations_url = api_base_url + "movie/" + str(movie_id) + "/recommendations?"

    params = {
    "api_key": api_key,
    "language": "en-US",
    "casts": "casts",
    }

    movie = requests.get(movie_detail_url, params=params).json()
    movie_casts = requests.get(movie_casts_url, params=params).json().get("cast", [] )[:4]
    movie_crew = requests.get(movie_casts_url, params=params).json().get("crew", [] )
    trailers_data = requests.get(trailers_url, params=params).json().get("results", [])
    recommendations = requests.get(recommendations_url, params=params).json().get("results", [])

    context = { 
        "movie": movie, "image_base_url": image_base_url,
        "movie_casts": movie_casts,
        "movie_crew": movie_crew,
        "trailers": trailers_data,
        "recommendations": recommendations,
        }

    return render(request,'movies/movie_detail.html', context)

def search_movies(request):
    query = request.GET.get('query')
    search_movies = []
    page_number = request.GET.get('page', 1)
    params = {
        "api_key": api_key,
        "language": "en-US",
        "query": query,
        "page": f'{page_number}',
    }
    search_movies_url = api_base_url + "search/movie?"
    response = requests.get(search_movies_url, params=params)
    if response.status_code == 200:
        data = response.json()
        search_movies = data.get('results', [])
        total_pages = data['total_pages']
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = {
                'page': int(page_number),
                'total_pages': total_pages,
                'movie': search_movies,
                'image_base_url': image_base_url,
                'has_next': int(page_number) < total_pages,
                'next_page':int(page_number) + 1 if int(page_number) < total_pages else None,
                'query': query, 
            }
            return JsonResponse(context)
        context = {
            'movies': search_movies,
            'image_base_url': image_base_url,
            'has_next': int(page_number) < total_pages,
            'next_page':int(page_number) + 1 if int(page_number) < total_pages else None,
            'query': query,
        }

        return render(request, 'movies/search_movies.html', context)
    else:
        # Handling the error gracefully
        context = {
            'error': 'Unable to fetch search movies at the moment'
        }
        return render(request, 'movies/search_movies.html', context)


def proxy_search(request):
    query = request.GET.get('query')
    params = {
        "api_key": api_key,
        "language": "en-US",
        "query": query,
    }

    if query:
        tmdb_url = api_base_url + "search/movie"
        response = requests.get(tmdb_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        return JsonResponse({'error': 'Failed to fetch data from TMDB'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def genre_movies(request, genre_id):

    # TMDB endpoint for genres
    genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US'
    page_number = request.GET.get('page', 1)
    params = {
    "api_key": api_key,
    "language": "en-US",
    "sort_by": "popularity.desc",
    "page": f'{page_number}', 
    "with_genres": f'{genre_id}',
    "year": 2024   
    }

    # Get the list of genres to find the specific genre
    response = requests.get(genre_url)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        genre = next((g for g in genres if g['id'] == genre_id), None) # next: returns the first match or none if there is no matchafter iteration

        # TMDB endpoint for movies in the specified genre
        # movies_url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}&year=2024&sort_by=popularity.desc'
        
        movies_url = api_base_url + "discover/movie?"


        # Get the list of movies in the specified genre
        movies_data = requests.get(movies_url, params=params).json()
        total_pages = movies_data.get('total_pages', 1)
        movies = movies_data.get('results', [])
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
            # Create context with genre and movies
            context = {
                'movie': movies,
                'image_base_url': image_base_url,
                'page': int(page_number),
                'total_pages': total_pages,
                'has_next': int(page_number) < total_pages,
                'next_page':int(page_number) + 1 if int(page_number) < total_pages else None,

            }
            
            # Return Json reaponae of the context data
            return JsonResponse(context)
        

        # Create context with genre and movies
        context = {
            'image_base_url': image_base_url,
            'genre': genre,
            'movies': movies,
            'has_next': int(page_number) < total_pages,
            'next_page':int(page_number) + 1 if int(page_number) < total_pages else None,
        }
        
        # Render the 'genre_movies.html' template with the context data
        return render(request, 'movies/genre_movies.html', context)
    
    else:
        # Handling the case where there are no genres found
        context = {
            'error': f'unable to fectch {genre.name} movies at the moment'
        }
        return render(request, 'movies/genre_movies.html', context)
       

def movie_language(request, language_id):
    language_url = f'{api_base_url}configuration/languages?api_key={api_key}'
    page_number = request.GET.get('page', 1)

    # Get the list of languages
    response = requests.get(language_url)
    if response.status_code == 200:
        all_languages = response.json()
        language = next((l for l in all_languages if l['iso_639_1'] == language_id), None)
        print('language:', language)
        print('language_id:', language_id)
        
        if language:
            params = {
                "api_key": api_key,
                "sort_by": "popularity.desc",
                "page": f'{page_number}',
                "with_original_language": f'{language_id}',
            }
            
            movies_url = f"{api_base_url}discover/movie"
            movies_data = requests.get(movies_url, params=params).json()
            print('movies_url:', movies_url)
            print('movies_data:', movies_data)
            movies = movies_data.get('results', [])

            if movies:
                total_pages = movies_data.get('total_pages', 1)
                
                context = {
                    'image_base_url': image_base_url,
                    'language': language,
                    'movies': movies,
                    'page': int(page_number),
                    'total_pages': total_pages,
                    'has_next': int(page_number) < total_pages,
                    'next_page': int(page_number) + 1 if int(page_number) < total_pages else None,
                }
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    context = {
                        'movie': movies,
                        'image_base_url': image_base_url,
                        'page': int(page_number),
                        'total_pages': total_pages,
                        'has_next': int(page_number) < total_pages,
                        'next_page': int(page_number) + 1 if int(page_number) < total_pages else None,
                    }
                    return JsonResponse(context)

                return render(request, 'movies/language_movies.html', context)
            else:
                context = {'error': f'Unable to fetch movies for {language["english_name"]}'}
        else:
            context = {'error': f'Language with ID {language_id} not found'}
    else:
        context = {'error': 'Unable to fetch language data'}

    
    return render(request, 'movies/language_movies.html', context)
