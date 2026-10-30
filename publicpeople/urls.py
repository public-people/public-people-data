from ajax_select import urls as ajax_select_urls
from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page

from rest_framework import routers
from graphene_django.views import GraphQLView
from .views import (
    AboutView,
    AreaViewSet,
    ContactView,
    ContentTypeViewSet,
    LinkToPopoloSourceViewSet,
    MembershipViewSet,
    OrganizationViewSet,
    PersonSearchListView,
    PersonView,
    PersonViewSet,
    PopoloSourceViewSet,
    PostViewSet,
)
from .sitemap import PersonSitemap

CACHE_SECS = 60 * 60 * 24


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'posts', PostViewSet)
router.register(r'areas', AreaViewSet)
router.register(r'contenttypes', ContentTypeViewSet)
router.register(r'linktopopolosource', LinkToPopoloSourceViewSet)
router.register(r'popolosource', PopoloSourceViewSet)

urlpatterns = [
    re_path('^$',
        cache_page(CACHE_SECS)(PersonSearchListView.as_view()),
        name='person_list'),
    re_path(r'^person/(?P<person_id>\d+)-(?P<name_slug>[\w-]+)',
        cache_page(CACHE_SECS)(PersonView.as_view()),
        name='person'),

    re_path(r'^about$', AboutView.as_view(), name='about'),
    re_path(r'^contact$', ContactView.as_view(), name='contact'),

    re_path(r'^ajax_select/', include(ajax_select_urls)),
    re_path(r'^admin/', admin.site.urls),


    re_path(r'^api/', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^graphql', GraphQLView.as_view(graphiql=True)),

    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': {'persons': PersonSitemap}},
        name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DJANGO_DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
