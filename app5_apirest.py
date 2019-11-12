#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
app.py by laurent
"""

import mysql.connector
import argparse
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import locale
from isodate import parse_duration

from entities.movie import Movie
from entities.person import Person
from entities.scrapper import Scrapper
from entities import themoviedb


def connect_to_database():
    return mysql.connector.connect(
        user='predictor', password='predictor',
        host='database', database='predictor')


def create_cursor(cnx):
    return cnx.cursor(named_tuple=True)


def disconnect_to_database(cnx, cursor):
    cursor.close()
    cnx.close()


def find_query(table, id):
    return f"SELECT * FROM {table} WHERE id={id} LIMIT 1"


def find(table, id):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)

    query = find_query(table, id)
    cursor.execute(query)
    result = cursor.fetchall()

    entity = None
    if cursor.rowcount == 1:
        if table == "movies":
            entity = Movie(
                    imdb_id=result[0].imdb_id,
                    original_title=result[0].original_title,
                    title=result[0].title,
                    duration=result[0].duration,
                    release_date=result[0].release_date,
                    rating=result[0].rating
                )

        if table == "people":
            entity = Person(
                firstname=result[0].firstname, lastname=result[0].lastname
                )

        entity.id = result[0].id

    disconnect_to_database(cnx, cursor)
    return entity


def findall(table):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    cursor.execute(f"SELECT * FROM {table}")
    results = cursor.fetchall()
    disconnect_to_database(cnx, cursor)

    entities = None
    if table == "movies":
        entities = []
        for result in results:
            entity = Movie(
                imdb_id=result.imdb_id,
                original_title=result.original_title,
                title=result.title,
                duration=result.duration,
                release_date=result.release_date,
                rating=result.rating
            )
            entity.id = result.id
            entities += [entity]

    if table == "people":
        entities = []
        for result in results:
            entity = Person(
                firstname=result.firstname, lastname=result.lastname
                )
            entity.id = result.id
            entities += [entity]

    return entities


def find_imdbid(imdb_id, cnx=None, cursor=None):
    to_close = False
    if cnx is None:
        cnx = connect_to_database()
        cursor = create_cursor(cnx)
        to_close = True

    query = ("SELECT * FROM `movies` WHERE `imdb_id`=%(imdbid)s")
    data = {'imdbid': imdb_id}
    cursor.execute(query, params=data)
    result = cursor.fetchall()

    if cursor.rowcount == 1:
        result = Movie(
                    imdb_id=result[0].imdb_id,
                    original_title=result[0].original_title,
                    title=result[0].title,
                    duration=result[0].duration,
                    release_date=result[0].release_date,
                    rating=result[0].rating
                )
    else:
        result = None

    if to_close:
        disconnect_to_database(cnx, cursor)

    return result


def insert_people(person):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)
    query = "INSERT INTO `people` (`firstname`, `lastname`) VALUES (%s, %s)"
    data = (person.firstname, person.lastname)
    cursor.execute(query, params=data)
    lastId = cursor.lastrowid
    cnx.commit()
    disconnect_to_database(cnx, cursor)
    return lastId


def insert_movie(movie):
    cnx = connect_to_database()
    cursor = create_cursor(cnx)

    imdb_check = find_imdbid(movie.imdb_id, cnx, cursor)

    if imdb_check is not None:
        lastId = None

    else:

        query = ("INSERT INTO `movies` (`imdb_id`, `original_title`, `title`,"
                 "`duration`, `release_date`, `rating`, `is3d`,"
                 "`production_budget`, `marketing_budget`,"
                 "`synopsis`, `review`)"
                 "VALUES (%(imdb_id)s, %(original_title)s, %(title)s,"
                 "%(duration)s, %(release_date)s, %(rating)s, %(is3d)s,"
                 "%(production_budget)s, %(marketing_budget)s,"
                 "%(synopsis)s, %(review)s)"
                 )
        data = {
            'imdb_id': movie.imdb_id,
            'original_title': movie.original_title,
            'title': movie.title,
            'duration': movie.duration,
            'release_date': movie.release_date,
            'rating': movie.rating,
            'is3d': movie.is3d,
            'production_budget': movie.production_budget,
            'marketing_budget': movie.marketing_budget,
            'synopsis': movie.synopsis,
            'review': movie.review
        }

        cursor.execute(query, params=data)
        lastId = cursor.lastrowid
        cnx.commit()

    disconnect_to_database(cnx, cursor)

    return lastId


def print_person(person):
    print(f"#{person.id}: {person.firstname} {person.lastname}")


def print_movie(movie):
    print(f"#{movie.id}: {movie.title} released on {movie.release_date}")


def scrap_movie(movie_url):
    locale.setlocale(locale.LC_ALL, locale='en_US')

    # https://www.imdb.com/title/tt7016254
    # https://www.imdb.com/title/tt2527338

    imdb_id = movie_url

    scrapper = Scrapper(movie_url)
    r = scrapper.scrap()
    soup = BeautifulSoup(r.text, 'html.parser')

    # title
    title = soup.find("h1").contents[0].strip()

    # original_title
    if soup.find("div", class_="originalTitle"):
        original_title = soup.find("div", class_="originalTitle")\
            .contents[0].strip()
    else:
        original_title = title

    # duration
    duration_string = soup.find("time")['datetime']
    duration_object = parse_duration(duration_string)
    duration = int(duration_object.total_seconds()/60)

    # release_date
    release_date_string = soup.find(
        'a', title='See more release dates'
        ).contents[0]
    release_date_string = release_date_string.replace('(France)', '').strip()
    release_date_object = datetime.strptime(release_date_string, '%d %B %Y')
    release_date = datetime.strftime(release_date_object, '%Y-%m-%d')

    # rating
    rating_object = soup.find("div", class_="subtext")
    rating_string = rating_object.contents[0].strip()
    if '12' in rating_string:
        rating = '-12'
    elif '16' in rating_string:
        rating = '-16'
    elif '18' in rating_string:
        rating = '-18'
    else:
        rating = 'TP'

    new_movie = Movie(
        imdb_id=imdb_id, original_title=original_title, title=title,
        duration=duration, rating=rating, release_date=release_date)
    print_movie(new_movie)

    results = insert_movie(new_movie)
    print(results)


def import_current_movies():
    movies_id_list = themoviedb.movies_in_theatre()
    ids = []
    for movie_id in movies_id_list:
        movie = themoviedb.collect_from__themoviedb(movie_id)
        new_id = insert_movie(movie)
        ids += [new_id]

    return ids


def main():
    parser = argparse.ArgumentParser(
        description='Process Movies Predictor data')
    parser.add_argument(
        'context',
        choices=['people', 'movies', 'import'],
        help='La table concernée, people ou movies'
        )

    known_args = parser.parse_known_args()[0]

    if known_args.context == "import":
        parser.add_argument('--api', help='source api')
        parser.add_argument('--imdbid', help='the id of movie')

    else:
        fullaction = parser.add_subparsers(dest='action', help='fullaction')

        parser_find = fullaction.add_parser('find')
        parser_find.add_argument('id', type=int)

        parser_list = fullaction.add_parser('list')
        parser_list.add_argument('--export', type=str)

        import_parser = fullaction.add_parser(
            'import', help='Add data from csv file')
        import_parser.add_argument('--file', help='File with data')

        parser_scrapp = fullaction.add_parser('scrap')
        parser_scrapp.add_argument('--url', type=str)

        insert_parser = fullaction.add_parser(
            'insert', help='Add data in tables')

        if known_args.context == "people":
            insert_parser.add_argument(
                '--firstname',
                help='Person first name',
                required=True)
            insert_parser.add_argument(
                '--lastname',
                help='Person last name',
                required=True)

        if known_args.context == "movies":
            insert_parser.add_argument(
                '--imdb_id', help='Movie imdb id', required=True)
            insert_parser.add_argument(
                '--original-title', help='Movie original title', required=True)
            insert_parser.add_argument(
                '--title', default=None, help='Movie title')
            insert_parser.add_argument(
                '--duration', default=None, help='Movie duration')
            insert_parser.add_argument(
                '--origin-country', default=None, help='Movie origin country')
            insert_parser.add_argument(
                '--release-date', default=None, help='Movie release date')
            insert_parser.add_argument(
                '--rating', default=None, help='Movie rating')

    args = parser.parse_args()
    # print(args)

    """
    Args example:
    $ python app.py movies find 1
    $ python app.py people list
    $ python app.py people list --export "listing.csv"

    $ python app.py people insert --firstname "John" --lastname "Doe"
    $ python app.py movies insert
    --title "Star Wars, épisode VIII : Les Derniers Jedi"--duration 152
        --original-title "Star Wars: Episode VIII – The Last Jedi"
        --origin-country US
        --release-date

    $ python app.py movies import --file new_movies.csv
    $ python app.py movies scrap --url https://www.imdb.com/title/tt2527338/

    $ python app.py import --api omdb --imdbid tt7016254
    $ python app.py import --api themoviedb --imdbid tt7016254
    """

    # Utiliser arguments pour afficher des inputs
    if args.context == "people":
        print("Mode People")

        if args.action == "find":
            peopleId = args.id
            person = find("people", peopleId)
            if person is None:
                print("Cet id n'a pas été trouvé")
            else:
                print_person(person)

        if args.action == "list":
            results = findall("people")

            if args.export:
                with open(args.export, 'w', newline='\n', encoding='utf-8') \
                        as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['id', 'firstname', 'lastname'])
                    for person in results:
                        writer.writerow(
                            [person.id, person.firstname, person.lastname]
                            )

            else:
                for person in results:
                    print_person(person)

        if args.action == "insert":
            person = Person(firstname=args.firstname, lastname=args.lastname)
            results = insert_people(person)
            print(results)

    if args.context == "movies":
        print("Mode Movies")

        if args.action == "find":
            movieId = args.id
            movie = find("movies", movieId)
            if movie is None:
                print("Cet id n'a pas été trouvé")
            else:
                print_movie(movie)

        if args.action == "list":
            results = findall("movies")
            for movie in results:
                print_movie(movie)

            if args.export:
                with open(args.export, 'w', newline='\n', encoding='utf-8')\
                        as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(results[0]._fields)
                    for movie in results:
                        writer.writerow(movie)

        if args.action == "insert":
            new_movie = Movie(
                title=args.title,
                duration=args.duration,
                original_title=args.original_title,
                release_date=args.release_date,
                rating=args.rating
            )

            results = insert_movie(new_movie)
            print(results)

        if args.action == "import":
            with open(args.file, 'r', encoding='utf-8', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if reader.line_num == 1:
                        _ = row

                    else:
                        new_movie = Movie(
                            title=row['title'],
                            duration=row['duration'],
                            original_title=row['original_title'],
                            release_date=row['release_date'],
                            rating=row['rating']
                        )

                        results = insert_movie(new_movie)
                        print(results)

        if args.action == "scrap":
            scrap_movie(args.url)

    if args.context == "import":
        print('Mode import')
        if args.api == 'themoviedb':
            print('Mode themoviedb')
            movie = themoviedb.collect_from__themoviedb(args.imdbid)
            results = insert_movie(new_movie)
            print(results)
            print()


if __name__ == "__main__":
    main()
