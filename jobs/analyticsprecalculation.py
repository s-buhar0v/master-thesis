import os
import pymongo
import itertools

from datetime import datetime

client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])
db = client.masterthesis

CITIES_TOP_COUNT = 5
COUNTRIES_TOP_COUNT = 5
LANGUAGES_TOP_COUNT = 3

CURRENT_YEAR = datetime.utcnow().year
AGE_RANGES = [
    {
        'start': 0,
        'end': 16,
    },
    {
        'start': 17,
        'end': 21,
    },
    {
        'start': 22,
        'end': 35,
    },
    {
        'start': 36,
        'end': 60,
    },
    {
        'start': 61,
        'end': 75,
    },
    {
        'start': 76,
        'end': 90,
    },
    {
        'start': 90,
        'end': 1111,
    }
]


def _calculate_percentage(total, part, ndigits=1):
    return round(number=part / total * 100, ndigits=ndigits)


def _calculate_language_distribution(group_name):
    language_distribution = []

    users_with_filled_personal_data = list(
        db.users.find({'personal': {'$ne': None}, 'group_name': group_name}, {'personal': 1})
    )

    users_with_filled_languages = list(
        filter(lambda u: 'langs' in u['personal'], users_with_filled_personal_data)
    )
    languages = set(
        itertools.chain.from_iterable(
            map(lambda u: u['personal']['langs'], users_with_filled_languages)
        )
    )

    for language in languages:
        count = len(list(filter(lambda u: language in u['personal']['langs'], users_with_filled_languages)))
        language_distribution.append({
            'lang': language,
            'count': count,
        })

    language_distribution.sort(key=lambda l: l['count'])
    language_distribution_items_count = len(language_distribution)

    return {
        'top': language_distribution[
               language_distribution_items_count - LANGUAGES_TOP_COUNT: language_distribution_items_count],
        'others': language_distribution[0: language_distribution_items_count - LANGUAGES_TOP_COUNT],
    }


def _calculate_cities_distribution(group_name):
    cities_distribution = []

    users_with_filled_city = list(db.users.find({'city': {'$ne': None}, 'group_name': group_name}, {'city': 1}))
    cities = set(map(lambda c: c['city']['title'], users_with_filled_city))

    for city in cities:
        count = len(list(filter(lambda u: u['city']['title'] == city, users_with_filled_city)))
        cities_distribution.append({
            'city': city,
            'count': count,
        })

    cities_distribution.sort(key=lambda c: c['count'])
    cities_distribution_items_count = len(cities_distribution)

    return {
        'top': cities_distribution[
               cities_distribution_items_count - CITIES_TOP_COUNT: cities_distribution_items_count],
        'others': cities_distribution[0: cities_distribution_items_count - CITIES_TOP_COUNT],
    }


def _calculate_countries_distribution(group_name):
    countries_distribution = []

    users_with_filled_country = list(db.users.find({'country': {'$ne': None}, 'group_name': group_name}, {'country': 1}))
    countries = set(map(lambda c: c['country']['title'], users_with_filled_country))

    for country in countries:
        count = len(list(filter(lambda u: u['country']['title'] == country, users_with_filled_country)))
        countries_distribution.append({
            'country': country,
            'count': count,
        })

    countries_distribution.sort(key=lambda c: c['count'])
    countries_distribution_items_count = len(countries_distribution)

    return {
        'top': countries_distribution[
               countries_distribution_items_count - COUNTRIES_TOP_COUNT: countries_distribution_items_count],
        'others': countries_distribution[0: countries_distribution_items_count - CITIES_TOP_COUNT],
    }


def _calculate_age_distribution(group_name):
    age_distribution = []
    users_with_full_bdates = list(db.users.find({'bdate': {'$regex': '\d{1,2}.\d{1,2}.\d{4}'}, 'group_name': group_name}))

    for user_with_full_bday in users_with_full_bdates:
        user_with_full_bday['age'] = CURRENT_YEAR - int(user_with_full_bday['bdate'].split('.')[2])

    for age_range in AGE_RANGES:
        start = age_range['start']
        end = age_range['end']

        age_distribution.append({
            'range': f'{start} - {end}',
            'count': len(
                list(
                    filter(lambda u: start < u['age'] < end, users_with_full_bdates)
                )
            )
        })

    age_distribution_items_count = len(age_distribution)
    age_distribution.sort(key=lambda a: a['count']),

    return {
        'top': age_distribution[age_distribution_items_count - 1],
        'others': age_distribution[0:age_distribution_items_count - 1],
    }


def _calculate_gender_distribution(group_name):
    total_users_count = db.users.count_documents({'group_name': group_name})
    females = db.users.count_documents({'sex': 1})
    males = db.users.count_documents({'sex': 2})

    return {
        'males': males,
        'females': females,
        'total': total_users_count
    }


def _calculate_higher_education_percentage(total_users_count, group_name):
    users_with_filled_universities = db.users.count_documents({'universities': {'$ne': []}, 'group_name': group_name})

    return _calculate_percentage(total=total_users_count, part=users_with_filled_universities)


def _calculate_relation_percentage(total_users_count, group_name):
    # see https://vk.com/dev/objects/user_2
    users_in_relation = db.users.count_documents({'relation': {'$in': [2, 3, 4, 7, 8]}, 'group_name': group_name})

    return _calculate_percentage(total=total_users_count, part=users_in_relation)


def _calculate_social_networks_connections_percentage(total_users_count, group_name):
    # see https://vk.com/dev/objects/user_2
    return {
        'skype': _calculate_percentage(total=total_users_count, part=(
            db.users.count_documents({'skype': {'$ne': None}, 'group_name': group_name}))),
        'facebook': _calculate_percentage(total=total_users_count, part=(
            db.users.count_documents({'facebook': {'$ne': None}, 'group_name': group_name}))),
        'twitter': _calculate_percentage(total=total_users_count, part=(
            db.users.count_documents({'twitter': {'$ne': None}, 'group_name': group_name}))),
        'livejournal': _calculate_percentage(total=total_users_count, part=(
            db.users.count_documents({'livejournal': {'$ne': None}, 'group_name': group_name}))),
        'instagram': _calculate_percentage(total=total_users_count, part=(
            db.users.count_documents({'instagram': {'$ne': None}, 'group_name': group_name}))),
    }


def main():

    groups = db.groups.find({})

    for g in groups:
        total_users_count = db.users.count_documents({'group_name': g['group']})
        db.analytics.update_one(
            {
                'group': g['group'],
            },
            {
                '$set': {
                    'total_user_count': total_users_count,
                    'gender_distribution': _calculate_gender_distribution(group_name=g['group']),
                    'higher_education_percentage': _calculate_higher_education_percentage(
                        total_users_count=total_users_count,
                        group_name=g['group']
                    ),
                    'in_relation_percentage': _calculate_relation_percentage(
                        total_users_count=total_users_count,
                        group_name=g['group']
                    ),
                    'social_networks_connection_percentage':
                        _calculate_social_networks_connections_percentage(total_users_count=total_users_count, group_name=g['group']),
                    'cities_distribution': _calculate_cities_distribution(group_name=g['group']),
                    'countries_distribution': _calculate_countries_distribution(group_name=g['group']),
                    'age_distribution': _calculate_age_distribution(group_name=g['group']),
                    'lang_distribution': _calculate_language_distribution(group_name=g['group']),
                    'last_update': datetime.utcnow().isoformat(),
                    'group':  g['group'],
                }
            },
            upsert=True
        )


if __name__ == '__main__':
    main()
