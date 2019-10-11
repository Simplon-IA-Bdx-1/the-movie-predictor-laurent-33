print("zedz")
#import sqlalchemy
#print(sqlalchemy.__version__)
#engine = sqlalchemy.create_engine('mysql://predictor:predictor@localhost:3306/database/predictor', echo=True)

import mysql.connector

# insérer un people dans database
"""
cnx = mysql.connector.connect(user='predictor', password='predictor',
                              host='127.0.0.1',
                              database='predictor')
cursor = cnx.cursor()

# visualiser données
query = ("SELECT id, title, release_date FROM movies ")

cursor.execute(query)

for (id, title, release_date) in cursor:
  print("{}, {} was released on {:%d %b %Y}".format(
    id, title, release_date))

# insérer people
add_people = ("INSERT INTO people"
              "(firstname, lastname)"
              "VALUES (%s, %s)")

data_people = ('Clint', 'Eastwood')

cursor.execute(add_people, data_people)

# visualiser modif
query = ("SELECT id, firstname, lastname FROM people")
cursor.execute(query)

for (id, firstname, lastname) in cursor:
  print("{}, {}, {}".format(id, firstname, lastname))

#cnx.commit()
#cnx.rollback()
cursor.close()
cnx.close()
"""

#import sys
# for arg in sys.argv:
#   print(arg)

import argparse
parser = argparse.ArgumentParser(description='Process Movies Predictor data')
parser.add_argument('context', choices=['people', 'movies'], help='La table concernée, people ou movies')

fullaction = parser.add_subparsers(dest='action', help='fullaction')

parser_find = fullaction.add_parser('find')
parser_find.add_argument('id', type=int)

parser_list = fullaction.add_parser('list')
parser_list.add_argument('--export', type=str)

args = parser.parse_args()
print(args)

def connectToDatabase():
  return mysql.connector.connect(user='predictor', password='predictor',
                              host='127.0.0.1',
                              database='predictor')

def createCursor(cnx):
  return cnx.cursor(named_tuple=True)

def disconnectDatabase(cnx, cursor):
  cnx.close()

def closeCursor(cursor):
  cursor.close()

def findQuery(table, id):
  return f"SELECT * FROM {table} WHERE id = {id}"

def find(table, id):
  cnx = connectToDatabase()
  cursor = createCursor(cnx)
  cursor.execute(findQuery(table, id))
  results = cursor.fetchall()
  closeCursor(cursor)
  disconnectDatabase(cnx, cursor)
  return results

def findall(table):
  cnx = connectToDatabase()
  cursor = createCursor(cnx)
  cursor.execute(f"SELECT * FROM {table}")
  results = cursor.fetchall()
  closeCursor(cursor)
  disconnectDatabase(cnx, cursor)
  return results

import csv

# Utiliser arguments pour afficher des inputs
if args.context == "people":
  print("Mode People")
  
  if args.action == "find":
    peopleId = args.id

    results = find("people", peopleId)
    for person in results:
      print(f"#{person.id}: {person.firstname} {person.lastname}")

  if args.action == "list":
    results = findall("people")

    if args.export:
      with open(args.export, 'w', newline='\n', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(results[0]._fields)
        for person in results:
          writer.writerow(person)

    else:
      for person in results:
        print(f"#{person.id}: {person.firstname} {person.lastname}")

if args.context == "movies":
  print("Mode Movies")
  
  if args.action == "find":
    movieId = args.id

    results = find("movies", movieId)
    for movie in results:
      print("")
      print(movie)


