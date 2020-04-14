import os
import pymongo

from flask import Flask, jsonify, render_template

app = Flask(__name__, static_folder='static')
client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])


def _get_distribution_top(distribution, field):
    return list(
        map(lambda d: d[field], distribution['top'])
    )


@app.route('/api/analyze')
def analyze():
    analytics = client.masterthesis.analytics.find_one({})
    return jsonify({k: v for k, v in analytics.items() if k != '_id'}), 200


@app.route('/app')
def main():
    return render_template(
        template_name_or_list='index.html'
    )


@app.route('/app/analytics')
def analytics():
    group_analytics = client.masterthesis.analytics.find({})

    typical_users = list(map(lambda g: {
        'group': g['group'],
        'gender':
            'Male' if g['gender_distribution']['males'] > g['gender_distribution']['females'] else 'Female',
        'age': g['age_distribution']['top']['range'],
        'possible_cities': ', '.join(
            _get_distribution_top(
                distribution=g['cities_distribution'],
                field='city'
            )
        ),
        'possible_countries': ', '.join(
            _get_distribution_top(
                distribution=g['countries_distribution'],
                field='country'
            ),
        ),
        'higher_education': 'Yes' if g['higher_education_percentage'] > 50 else 'No',
        'in_relation': 'Yes' if g['in_relation_percentage'] > 50 else 'No',
        'possible_languages': ', '.join(
            _get_distribution_top(
                distribution=g['lang_distribution'],
                field='lang'
            )
        )
    }, group_analytics))

    print(typical_users)

    return render_template(
        template_name_or_list='analytics.html',
        typical_users=typical_users
    )
