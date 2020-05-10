import popolo
from django.db.models import Q
from popolo.models import Membership


class Person(popolo.models.Person):
    class Meta:
        proxy = True

    def current_memberships(self):
        return Membership.objects.filter(
            person=self
        ).filter(
            Q(end_date__exact='') | Q(end_date__isnull=True)
        ).order_by('-start_date').all()

    def ended_memberships(self):
        return Membership.objects.filter(
            person=self
        ).exclude(
            (Q(end_date__exact='') | Q(end_date__isnull=True))
        ).order_by('-end_date').all()

    def pa_url(self):
        pa_identifier_queryset = self.identifiers.filter(scheme="pombola-slug")
        if pa_identifier_queryset:
            return "https://pa.org.za/person/%s/" % pa_identifier_queryset.get().identifier
