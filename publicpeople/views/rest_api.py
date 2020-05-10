from django.contrib.contenttypes.models import ContentType
from popolo.models import Area, Membership, Organization, Post
from popolo_sources.models import LinkToPopoloSource, PopoloSource
from publicpeople.models import Person
from rest_framework import serializers, viewsets


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
