import graphene
from graphene_django.types import DjangoObjectType
from popolo.models import (Area, AreaI18Name, ContactDetail, Identifier,
                           Language, Link, Membership, Organization, OtherName,
                           Person, Post, Source)


class PersonType(DjangoObjectType):
    class Meta:
        model = Person

class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class MembershipType(DjangoObjectType):
    class Meta:
        model = Membership

class ContactDetailType(DjangoObjectType):
    class Meta:
        model = ContactDetail

class OtherNameType(DjangoObjectType):
    class Meta:
        model = OtherName

class IdentifierType(DjangoObjectType):
    class Meta:
        model = Identifier

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class SourceType(DjangoObjectType):
    class Meta:
        model = Source

class LanguageType(DjangoObjectType):
    class Meta:
        model = Language

class AreaType(DjangoObjectType):
    class Meta:
        model = Area

class AreaI18NameType(DjangoObjectType):
    class Meta:
        model = AreaI18Name

class Query(graphene.ObjectType):
    person = graphene.Field(PersonType,
                            id=graphene.Int())

    def resolve_person(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Person.objects.get(pk=id)

        return None

schema = graphene.Schema(query=Query)
