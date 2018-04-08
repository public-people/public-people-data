from popolo.models import (
    Organization,
    Membership,
    Person,
    Post,
    Area,
)
from popolo_sources.models import LinkToPopoloSource, PopoloSource
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, serializers
import operator
from django.db.models import Q
from functools import reduce
from django.views.generic.list import ListView
from django.utils.text import slugify
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.urls import reverse
import requests


class PersonView(TemplateView):
    template_name = "person.html"

    def get_context_data(self, **kwargs):
        person = get_object_or_404(Person, pk=kwargs['person_id'])
        memberships = person.memberships.order_by('end_date')
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

        r = requests.get('https://alephapi.public-people.techforgood.org.za/api/2/search',
                         params={
                             'q': '"%s"' % person.name,
                             'sort': 'published_at',
                             'limit': 1000,
                         })
        r.raise_for_status()
        for article in r.json()['results']:
            events.append({
                'type': 'article',
                'article': article,
                'date': article['published_at'],
            })
        events = sorted(events, key=lambda e: e['date'], reverse=True)

        context = super(TemplateView, self).get_context_data(**kwargs)
        context['person'] = person
        context['events'] = events
        return context


class PersonSearchListView(ListView):
    """
    Display a Person List page filtered by the search query.
    """
    model = Person
    paginate_by = 10

    def get_queryset(self):
        result = super(PersonSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
            )

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
        return data


# API VIEWS

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


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
