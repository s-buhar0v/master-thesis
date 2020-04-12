import os
import pymongo

from datetime import datetime

client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])
db = client.masterthesis

CITIES_TOP_COUNT = 5
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
group_name = 'w220.club'


def _calculate_percentage(total, part, ndigits=1):
    return round(number=part / total * 100, ndigits=ndigits)


def main():
    age_distribution = []
    cities_distribution = []

    total_users_count = db.users.count_documents({})
    females = db.users.count_documents({'sex': 1})
    males = db.users.count_documents({'sex': 2})
    has_higher_education = db.users.count_documents({'universities': {'$ne': []}})
    users_with_full_bdates = list(db.users.find({'bdate': {'$regex': '\d{1,2}.\d{1,2}.\d{4}'}}))

    users_with_city = list(db.users.find({'city': {'$ne': None}}, {'city': 1}))
    cities = set(map(lambda c: c['city']['title'], users_with_city))

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

    for city in cities:
        count = len(list(filter(lambda u: u['city']['title'] == city, users_with_city)))
        cities_distribution.append({
            'city': city,
            'percentage': _calculate_percentage(total=len(users_with_city), part=count)
        })

    cities_distribution.sort(key=lambda c: c['percentage']),
    cities_distribution_items_count = len(cities_distribution)
    age_distribution.sort(key=lambda a: a['count']),
    age_distribution_items_count = len(age_distribution)

    db.analytics.update_one(
        {
            'group': group_name
        },
        {
            '$set': {
                'last_update': datetime.utcnow().isoformat(),
                'males_percentage': _calculate_percentage(total=total_users_count, part=males),
                'females_percentage': _calculate_percentage(total=total_users_count, part=females),
                'has_higher_education_percentage': _calculate_percentage(
                    total=total_users_count,
                    part=has_higher_education
                ),
                'cities_distribution': {
                    'top': cities_distribution[cities_distribution_items_count - CITIES_TOP_COUNT: cities_distribution_items_count],
                    'others': cities_distribution[0:cities_distribution_items_count - CITIES_TOP_COUNT],
                },
                'age_distribution': {
                    'top': age_distribution[age_distribution_items_count - 1],
                    'others': age_distribution[age_distribution_items_count - 1],
                },
                'group': 'w220.club'
            }
        },
        upsert=True
    )


if __name__ == '__main__':
    main()
