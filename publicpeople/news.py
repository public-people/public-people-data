import requests
import logging

logger = logging.getLogger(__name__)

PAGE_SIZE = 500

class NewsSearch():

    @classmethod
    def search(cls, query, offset):
        session = requests.Session()
        r = session.get('https://alephapi.public-people.techforgood.org.za/api/2/search',
                             params={
                                 'q': '"%s"' % query,
                                 'sort': 'published_at:desc',
                                 'limit': PAGE_SIZE,
                                 'offset': offset,
                             })
        r.raise_for_status()
        response = r.json()
        prev_offset = cls._prev_offset(offset)
        next_offset = cls._next_offset(offset, response['total'])
        return {
            'items': response['results'],
            'prev_offset': prev_offset,
            'next_offset': next_offset,
            'page_number': response['page'],
            'total_pages': response['pages'],
        }

    @staticmethod
    def _next_offset(offset, total):
        next_offset = offset + PAGE_SIZE
        if next_offset >= total:
            next_offset = None
        return next_offset

    @staticmethod
    def _prev_offset(offset):
        prev_offset = offset - PAGE_SIZE
        if prev_offset < 0:
            prev_offset = 0
        if prev_offset == offset:
            prev_offset = None
        return prev_offset
