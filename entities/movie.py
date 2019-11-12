class Movie:
    def __init__(self, imdb_id, original_title=None, title=None,
                 duration=None, release_date=None, rating=None,
                 actors=[], productor=[], is3d=None,
                 production_budget=None, marketing_budget=None,
                 synopsis=None, review=None):

        self.id = None

        self.imdb_id = imdb_id
        self.title = title
        self.original_title = original_title
        self.title = title
        self.duration = duration
        self.release_date = release_date
        self.rating = rating

        # self.actors = actors
        # self.productor = productor
        self.is3d = is3d
        self.production_budget = production_budget
        self.marketing_budget = marketing_budget
        self.synopsis = synopsis
        self.review = review

    def total_budget(self):
        if self.production_budget is None or self.marketing_budget is None:
            return None

        return self.production_budget + self.marketing_budget
