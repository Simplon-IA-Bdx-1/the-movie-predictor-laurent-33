import requests
from entities.movie import Movie


def import_themoviedb(imdbid):
    serveur = 'https://api.themoviedb.org'
    api_version = '/3'
    ressource = '/movie/' + imdbid
    query = '?external_source=imdb_id'
    headers_info = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': themoviedbaccess
    }
    url = serveur + api_version + ressource + query
    json_infos = requests.get(url, headers=headers_info)

    return json_infos


def parse_themoviedb(infos):
    result = Movie(
        imdb_id=infos['imdb_id'],
        original_title=infos['original_title'],
        title=infos['title'],
        duration=None,
        release_date=infos['release_date'],
        rating=None
        )
    result.synopsis = infos['overview']
    result.review = infos['vote_average']

    return result


def collect_from__themoviedb(movie_id):
    result = import_themoviedb(movie_id).json()
    movie = parse_themoviedb(result)
    return movie


def movies_in_theatre():
    serveur = 'https://api.themoviedb.org'
    api_version = '/3'
    ressource = '/movie/now_playing'
    query = ''
    headers_info = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': themoviedbaccess
    }
    url = serveur + api_version + ressource + query
    movies_list = requests.get(url, headers=headers_info).json()['results']

    movies_id_list = []
    for movie in movies_list:
        movies_id_list += [str(movie['id'])]

    return movies_id_list


with open('auth.env', 'r') as file:
    for line in file:
        variable, value = line.split('=')
        if variable == 'TMDB_ACCESS_KEY':
            themoviedbaccess = 'Bearer ' + value.strip()
