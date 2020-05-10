from popolo.models import (
    Organization,
    Membership,
    Post,
    Area,
)
from .models import (
    Person,
)

from .news_api import NewsSearch
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from functools import reduce
from popolo_sources.models import LinkToPopoloSource, PopoloSource
from rest_framework import viewsets, serializers
import operator
from .timeline import (
    get_search_query,
    get_timeline,
)


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
        context = super(TemplateView, self).get_context_data(**kwargs)
        person = get_object_or_404(Person, pk=kwargs['person_id'])
        memberships = person.memberships.order_by('end_date')

        news_offset = int(self.request.GET.get('offset', '0'))
        search_query = get_search_query(person)
        results = NewsSearch.search(search_query, offset=news_offset)
        is_first_page = results["prev_offset"] is None
        is_last_page = results["next_offset"] is None
        date_groups = get_timeline(results["items"], memberships, is_first_page, is_last_page)

        context['person'] = person
        context['pa_url'] = person.pa_url()
        context['date_groups'] = date_groups
        context['name_query'] = search_query
        context['next_url'] = pagination_url(self.request, results['next_offset'])
        context['prev_url'] = pagination_url(self.request, results['prev_offset'])
        context['page_number'] = results['page_number']
        context['total_pages'] = results['total_pages']
        return context


def pagination_url(request, offset):
    if offset is None:
        return None
    params = request.GET.copy()
    params['offset'] = offset
    querystring = params.urlencode()
    return "{}?{}".format(request.path, querystring)


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
            return obj.get_absolute_url()
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
