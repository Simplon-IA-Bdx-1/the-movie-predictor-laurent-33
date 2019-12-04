import requests
from datetime import datetime, timedelta
from entities.movie import Movie


def import_themoviedb(imdbid):
    serveur = 'https://api.themoviedb.org'
    api_version = '/3'
    ressource = '/movie/' + str(imdbid)
    query = '?external_source=imdb_id'
    headers_info = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': themoviedbaccess
    }
    url = serveur + api_version + ressource + query
    json_infos = requests.get(url, headers=headers_info).json()
    
    if 'status_code' in json_infos.keys():
        print(json_infos['status_message'])

    return json_infos


def parse_themoviedb(infos, id_type='id'):
    result = Movie(
        imdb_id=infos[id_type],
        original_title=infos['original_title'],
        title=infos['title'],
        duration=None,
        release_date=infos['release_date'],
        rating=None
        )
    result.synopsis = infos['overview']
    result.review = infos['vote_average']

    return result


def collect_from_themoviedb(movie_id, id_type='imdb_id'):
    result = import_themoviedb(movie_id)
    if 'imdb_id' in result.keys():
        movie = parse_themoviedb(result, id_type='imdb_id')
    else:
        movie = None

    return movie


def movies_in_theatre():
    movies_id, total_pages = movies_in_theatre_by_page(page_number=1)
    print(f'page : 1 /{total_pages}')

    for page in range(1, total_pages + 1):
        print(f'page : {page} /{total_pages}')
        movies_id_page, _ = movies_in_theatre_by_page(page)
        movies_id += movies_id_page

    return movies_id


def movies_since(date):
    movies_id, total_pages = movies_since_by_page(date, page_number=1)
    print(f'page : 1 /{total_pages}')

    for page in range(1, total_pages + 1):
        print(f'page : {page} /{total_pages}, - date : {date}')
        movies_id_page, _ = movies_since_by_page(date, page)
        movies_id += movies_id_page

    return movies_id


def movies_since_by_page(date, page_number=1):
    serveur = 'https://api.themoviedb.org'
    api_version = '/3'
    ressource = '/discover/movie'
    query = f'?primary_release_date.gte={date}&primary_release_date.lte={datedelaveille}&page={page_number}'
    headers_info = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': themoviedbaccess
    }
    url = serveur + api_version + ressource + query
    movies_list = requests.get(url, headers=headers_info).json()
    
    if 'status_code' in movies_list.keys():
        print(movies_list['status_message'])

    if page_number == 1:
        total_pages = movies_list['total_pages']
    else:
        total_pages = None
    movies_list = movies_list['results']

    movies_id = []
    for movie in movies_list:
        movies_id += [movie['id']]

    return movies_id, total_pages


def movies_in_theatre_by_page(page_number=1):
    serveur = 'https://api.themoviedb.org'
    api_version = '/3'
    ressource = '/movie/now_playing'
    query = '?page=' + str(page_number)
    headers_info = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': themoviedbaccess
    }
    url = serveur + api_version + ressource + query
    movies_list = requests.get(url, headers=headers_info).json()

    if 'status_code' in movies_list.keys():
        print(movies_list['status_message'])
        
    if page_number == 1:
        total_pages = movies_list['total_pages']
    else:
        total_pages = None
    movies_list = movies_list['results']

    movies_id = []
    for movie in movies_list:
        movies_id += [movie['id']]

    return movies_id, total_pages


datedelaveille = datetime.date(datetime.now()-timedelta(days=1))
print(datedelaveille)

with open('auth.env', 'r') as file:
    for line in file:
        variable, value = line.split('=')
        if variable == 'TMDB_ACCESS_KEY':
            themoviedbaccess = 'Bearer ' + value.strip()
