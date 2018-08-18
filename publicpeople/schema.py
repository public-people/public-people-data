import graphene

from graphene_django.types import DjangoObjectType

from popolo.models import (
    Person,
    Organization,
    Post,
    Membership,
    ContactDetail,
    OtherName,
    Identifier,
    Link,
    Source,
    Language,
    Area,
    AreaI18Name,
)


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
    all_persons = graphene.List(PersonType)
    all_organizations = graphene.List(OrganizationType)
    all_posts = graphene.List(PostType)
    all_memberships = graphene.List(MembershipType)

    def resolve_all_persons(self, info, **kwargs):
        return Person.objects.all()

    def resolve_all_organizations(self, info, **kwargs):
        return Organization.objects.all()

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_all_membershops(self, info, **kwargs):
        return Membership.objects.all()

schema = graphene.Schema(query=Query)
