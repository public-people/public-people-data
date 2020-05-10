from itertools import groupby
import json


def get_first_last_name(full_name):
    names = full_name.split(' ')
    if len(names) == 1:
        return names[0]
    return "%s %s" % (names[0], names[-1])


def get_search_query(person):
    return get_first_last_name(person.name)


def get_timeline(search_results, memberships, is_first_page, is_last_page):
    news_events = make_news_events(search_results)
    membership_events = make_membership_events(memberships)
    events = membership_events + news_events
    events = sorted(events, key=lambda e: e['date'], reverse=True)
    if not is_first_page:
        events = drop_membership_before_news(events)
    if not is_last_page:
        events = drop_membership_after_news(events)

    return group_by_date(events)


def drop_membership_before_news(events):
    seen_news = False
    for event in events:
        if event["type"] == "article":
            seen_news = True
        if seen_news:
            yield event


def drop_membership_after_news(events):
    return reverse(drop_membership_before_news(reverse(events)))


def reverse(collection):
    return list(collection)[::-1]


def group_by_date(events):
    """Assumes events are sorted by date"""
    date_groups = []
    for date, group in groupby(events, lambda e: e['date'] and e['date'][:10]):
        date_groups.append({
            'date': date,
            'events': list(group),
        })
    return date_groups


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


def unique(list_of_dicts):
    uniques = {}
    for val in list_of_dicts:
        uniques[json.dumps(val, sort_keys=True)] = val
    return uniques.values()
