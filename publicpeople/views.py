from popolo.models import (
    Organization,
    Membership,
    Post,
    Area,
)
from .models import(
    Person,
)

from .news import NewsSearch
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from functools import reduce
from popolo_sources.models import LinkToPopoloSource, PopoloSource
from rest_framework import viewsets, serializers
import json
import operator
from itertools import groupby


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


class PersonView(TemplateView):
    template_name = "person.html"

    def get_context_data(self, **kwargs):
        person = get_object_or_404(Person, pk=kwargs['person_id'])
        memberships = person.memberships.order_by('end_date')
        membership_events = self.make_membership_events(memberships)

        first_last_name = get_first_last_name(person.name)
        news_offset = int(self.request.GET.get('offset', '0'))
        results = NewsSearch.search(first_last_name, offset=news_offset)
        news_events = self.make_news_events(results['items'])

        events = membership_events + news_events
        events = sorted(events, key=lambda e: e['date'], reverse=True)
        date_groups = []
        for date, group in groupby(events, lambda e: e['date'] and e['date'][:10]):
            date_groups.append({
                'date': date,
                'events': list(group),
            })
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['person'] = person
        context['date_groups'] = date_groups
        context['name_query'] = first_last_name
        context['next_url'] = pagination_url(self.request, results['next_offset'])
        context['prev_url'] = pagination_url(self.request, results['prev_offset'])
        context['page_number'] = results['page_number']
        context['total_pages'] = results['total_pages']
        return context

    @staticmethod
    def make_membership_events(memberships):
        events = []
        for membership in memberships:
            if membership.start_date:
                events.append({
                    'type': 'started',
                    'membership': membership,
                    'date': membership.start_date,
                })
            if membership.end_date:
                events.append({
                    'type': 'ended',
                    'membership': membership,
                    'date': membership.end_date,
                })
            if not (membership.start_date or membership.end_date):
                events.append({
                    'type': 'for all known time',
                    'membership': membership,
                    'date': None,
                })
        return events

    @staticmethod
    def make_news_events(news_items):
        news_events = []
        for article in news_items:
            news_events.append({
                'type': 'article',
                'article': article,
                'date': article['published_at'],
            })
        news_events = unique(news_events)
        return news_events


def pagination_url(request, offset):
    if offset is None:
        return None
    params = request.GET.copy()
    params['offset'] = offset
    querystring = params.urlencode()
    return "{}?{}".format(request.path, querystring)


def get_first_last_name(full_name):
    names = full_name.split(' ')
    if len(names) == 1:
        return names[0]
    return "%s %s" % (names[0], names[-1])


def unique(list_of_dicts):
    uniques = {}
    for val in list_of_dicts:
        uniques[json.dumps(val, sort_keys=True)] = val
    return uniques.values()


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


# API VIEWS

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    search_fields = (
        'label',
        'role',
        'person',
        'organization',
    )
    filter_fields = search_fields


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "id",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
            "name",
            "family_name",
            "given_name",
            "additional_name",
            "honorific_prefix",
            "honorific_suffix",
            "patronymic_name",
            "sort_name",
            "email",
            "gender",
            "birth_date",
            "death_date",
            "image",
            "summary",
            "biography",
            "national_identity",
            "memberships",
        )

    memberships = MembershipSerializer(many=True, read_only=True)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    search_fields = (
        'name',
        'other_names__name',
        'family_name',
        'given_name',
        'additional_name',
        'email'
    )
    filter_fields = search_fields


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    search_fields = (
        'name',
        'other_names__name',
        'classification',
    )
    filter_fields = search_fields


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer


class LinkToPopoloSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkToPopoloSource
        fields = '__all__'


class LinkToPopoloSourceViewSet(viewsets.ModelViewSet):
    queryset = LinkToPopoloSource.objects.all()
    serializer_class = LinkToPopoloSourceSerializer


class PopoloSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopoloSource
        fields = '__all__'


class PopoloSourceViewSet(viewsets.ModelViewSet):
    queryset = PopoloSource.objects.all()
    serializer_class = PopoloSourceSerializer


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"
