from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from .views import (
    PersonViewSet,
    OrganizationViewSet,
    MembershipViewSet,
    PostViewSet,
    AreaViewSet,
    ContentTypeViewSet,
)

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'posts', PostViewSet)
router.register(r'areas', AreaViewSet)
router.register(r'contenttypes', ContentTypeViewSet)

urlpatterns = [


    url(r'^admin/', admin.site.urls),


    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
