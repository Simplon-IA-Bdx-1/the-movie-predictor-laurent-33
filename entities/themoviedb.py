import requests
from entities.movie import Movie


def import_themoviedb(imdbid):
    with open('auth.env', 'r') as file:
        for line in file:
            variable, value = line.split('=')
            if variable == 'TMDB_ACCESS_KEY':
                themoviedbaccess = 'Bearer ' + value.strip()

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


def parse_themoviedb(json_infos, imdb_id):
    infos = json_infos

    result = Movie(
        imdb_id=imdb_id,
        original_title=infos['original_title'],
        title=infos['title'],
        duration=None,
        release_date=infos['release_date'],
        rating=None
        )
    result.synopsis = infos['overview']
    result.review = infos['vote_average']

    return result
