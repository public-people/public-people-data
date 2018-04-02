from django.conf.urls import url, include
from django.contrib import admin
from django.views import generic
from material.frontend import urls as frontend_urls

from rest_framework import routers
from .views import (
    PersonViewSet,
    OrganizationViewSet,
    MembershipViewSet,
    PostViewSet,
    AreaViewSet,
    ContentTypeViewSet,
    LinkToPopoloSourceViewSet,
    PopoloSourceViewSet,
)

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


    url(r'^admin/', admin.site.urls),


    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    url(r'^$', generic.RedirectView.as_view(url='/workflow/', permanent=False)),
    url(r'', include(frontend_urls)),
]
