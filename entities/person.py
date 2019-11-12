class Person:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        
        self.id = None
        self.movies = []

    def total_movies(self):
        return len(self.movies)
    