import json
from itertools import groupby

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from publicpeople.models import Person

from .news import NewsSearch


class PersonView(TemplateView):
    template_name = "person.html"

    def get_context_data(self, **kwargs):
        person = get_object_or_404(Person, pk=kwargs['person_id'])
        memberships = person.memberships.order_by('end_date')
        membership_events = self.make_membership_events(memberships)

        first_last_name = get_first_last_name(person.name)
        news_offset = int(self.request.GET.get('offset', '0'))
        results = NewsSearch.search(first_last_name, offset=news_offset)
        news_events = self.make_news_events(results['items'])

        events = membership_events + news_events
        events = sorted(events, key=lambda e: e['date'], reverse=True)
        date_groups = []
        for date, group in groupby(events, lambda e: e['date'] and e['date'][:10]):
            date_groups.append({
                'date': date,
                'events': list(group),
            })
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['person'] = person
        context['pa_url'] = person.pa_url()
        context['date_groups'] = date_groups
        context['name_query'] = first_last_name
        context['next_url'] = pagination_url(self.request, results['next_offset'])
        context['prev_url'] = pagination_url(self.request, results['prev_offset'])
        context['page_number'] = results['page_number']
        context['total_pages'] = results['total_pages']
        return context

    @staticmethod
    def make_membership_events(memberships):
        events = []
        for membership in memberships:
            if membership.start_date:
                events.append({
                    'type': 'started',
                    'membership': membership,
                    'date': membership.start_date,
                })
            if membership.end_date:
                events.append({
                    'type': 'ended',
                    'membership': membership,
                    'date': membership.end_date,
                })
            if not (membership.start_date or membership.end_date):
                events.append({
                    'type': 'for all known time',
                    'membership': membership,
                    'date': None,
                })
        return events

    @staticmethod
    def make_news_events(news_items):
        news_events = []
        for article in news_items:
            news_events.append({
                'type': 'article',
                'article': article,
                'date': article['published_at'],
            })
        news_events = unique(news_events)
        return news_events


def pagination_url(request, offset):
    if offset is None:
        return None
    params = request.GET.copy()
    params['offset'] = offset
    querystring = params.urlencode()
    return "{}?{}".format(request.path, querystring)


def get_first_last_name(full_name):
    names = full_name.split(' ')
    if len(names) == 1:
        return names[0]
    return "%s %s" % (names[0], names[-1])


def unique(list_of_dicts):
    uniques = {}
    for val in list_of_dicts:
        uniques[json.dumps(val, sort_keys=True)] = val
    return uniques.values()
