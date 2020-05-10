from django.contrib.sitemaps import Sitemap
from .models import Person


class PersonSitemap(Sitemap):

    def items(self):
        return Person.objects.all()
