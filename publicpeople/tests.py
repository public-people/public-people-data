from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, override_settings

from popolo.models import Membership, Organization, Person, Post


TEST_STORAGES = {
    **settings.STORAGES,
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

TEST_PIPELINE = {
    **settings.PIPELINE,
    'PIPELINE_ENABLED': False,
    'PIPELINE_COLLECTOR_ENABLED': False,
}


@override_settings(STORAGES=TEST_STORAGES, PIPELINE=TEST_PIPELINE)
class PublicPeopleTests(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name='Test Person')
        self.organization = Organization.objects.create(name='Test Organization')
        self.post = Post.objects.create(
            label='Member',
            organization=self.organization,
        )
        self.membership = Membership.objects.create(
            person=self.person,
            organization=self.organization,
            post=self.post,
            role='Member',
            start_date='2020-01-01',
        )

    def test_home_page(self):
        response = self.client.get('/', {'q': 'Test Person'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Person')

    def test_static_pages(self):
        for url in ('/about', '/contact'):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    @patch('publicpeople.views.NewsSearch.search')
    def test_person_page(self, search):
        search.return_value = {
            'items': [],
            'prev_offset': None,
            'next_offset': None,
            'page_number': 1,
            'total_pages': 1,
        }

        response = self.client.get(
            f'/person/{self.person.pk}-test-person')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Person')
        self.assertContains(response, 'Test Organization')

    def test_api(self):
        response = self.client.get('/api/persons/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

        response = self.client.get('/api/memberships/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

    def test_api_filtering(self):
        response = self.client.get('/api/persons/', {'name': 'Test Person'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

        response = self.client.get('/api/persons/', {'name': 'Someone Else'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_graphql(self):
        response = self.client.get(
            '/graphql',
            {'query': '{ person(id: %s) { name } }' % self.person.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['data']['person']['name'],
            'Test Person',
        )

    def test_sitemap(self):
        response = self.client.get('/sitemap.xml')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'/person/{self.person.pk}-test-person')
