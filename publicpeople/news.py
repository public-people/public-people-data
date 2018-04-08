import requests


class NewsSearch():
    def __init__(self, query):
        self.query = query
        self.idx = None
        self.items = None
        self.next_url = None

    def __iter__(self):
        return self

    def next(self):
        if self.items is None:
            r = requests.get('https://alephapi.public-people.techforgood.org.za/api/2/search',
                             params={
                                 'q': '"%s"' % self.query,
                                 'sort': 'published_at:desc',
                                 'limit': 100,
                             })
            r.raise_for_status()
            response = r.json()
            self.next_url = response['next']
            self.idx = 0
            self.items = response['results']

        if self.idx == len(self.items):
            if self.next_url:
                r = requests.get(self.next_url)
                r.raise_for_status()
                response = r.json()
                self.next_url = response['next']
                self.idx = 0
                self.items = response['results']
            else:
                raise StopIteration()

        item = self.items[self.idx]
        self.idx += 1
        return item
