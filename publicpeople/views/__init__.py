import operator
from functools import reduce

from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from publicpeople.models import Person

FEATURED_NAMES = [
    'Mduduzi Manana',
    'Jeff Radebe',
    'Faith Muthambi',
    'Trevor Manuel',
    'Vytjie Mentor',
    'Julius Malema',
    'Lindiwe Mazibuko',
    'Pravin Gordhan',
    'Manny de Freitas',
    'Magdalene Moonsamy',
    'Cheryllyn Dudley',
    'Qedani Dorothy Mahlangu',
    'Tasneem Motara',
    'Mary-Ann Dunjwa',
    'Leigh-Ann Mathys',
]


class PersonSearchListView(ListView):
    """
    Display a Person List page filtered by the search query.
    """
    model = Person
    paginate_by = 20

    def get_queryset(self):
        result = super(PersonSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
            )
        else:
            result = result.filter(name__in=FEATURED_NAMES)

        return result

    def get_context_data(self, **kwargs):
        def url(obj):
            return reverse('person', kwargs={
                'person_id': obj.id,
                'name_slug': slugify(obj.name),
            })
        data = super(PersonSearchListView, self).get_context_data(**kwargs)
        object_list = data['object_list']
        object_list = [{'obj': o, 'url': url(o)} for o in object_list]
        data['object_list'] = object_list
        data['q'] = self.request.GET.get('q') or ''
        return data


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"
