import requests

action_movies = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&year=2024&sort_by=popularity.desc&with_genres=28&api_key=92492102bdac5ee5e66f112789815a7e"

action = requests.get(action_movies).json().get("results", [])

print(action)