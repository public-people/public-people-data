import popolo
from popolo.models import Membership
from django.db.models import Q


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
