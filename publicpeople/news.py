import logging

import requests

logger = logging.getLogger(__name__)

PAGE_SIZE = 500


class NewsSearch():

    @classmethod
    def search(cls, query, offset):
        session = requests.Session()
        r = session.get('https://news.publicpeople.org.za/api/articles',
                        params={
                            'basic_web_search': '"%s"' % query,
                            'limit': PAGE_SIZE,
                            'offset': offset,
                        })
        r.raise_for_status()
        response = r.json()
        prev_offset = cls._prev_offset(offset)
        next_offset = cls._next_offset(offset, response['count'])
        return {
            'items': response['results'],
            'prev_offset': prev_offset,
            'next_offset': next_offset,
            'page_number': cls._page_number(offset),
            'total_pages': cls._page_count(response['count']),
        }

    @staticmethod
    def _page_number(offset):
        return int(offset / PAGE_SIZE + 1)

    @staticmethod
    def _page_count(item_count):
        return int(item_count / PAGE_SIZE + 1)

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
