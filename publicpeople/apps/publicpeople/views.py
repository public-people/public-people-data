from popolo.models import (
    Person,
    Organization,
    Membership,
    Post,
    Area,
)
from popolo_sources.models import LinkToPopoloSource, PopoloSource
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, serializers

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
