import requests


class Scrapper:

    def __init__(self, url):
        self.url = url

    def scrap(self):
        return requests.get(self.url)
