import os
import pymongo

from flask import Flask, jsonify, render_template, request, redirect, url_for
from socialmonitor.dataproviders.vk import VkDataExtractor

app = Flask(__name__, static_folder='static')
client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])
vk_data_extractor = VkDataExtractor()


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


@app.route('/app/group', methods=['GET'])
def group_list():
    groups = client.masterthesis.groups.find({})

    return render_template(
        template_name_or_list='groups.html',
        payload={'message': '', 'groups': groups}
    )


@app.route('/app/group', methods=['POST'])
def group_add():
    group = request.form['group']
    group_id = vk_data_extractor.get_group_id(group_name=group)
    message = ''

    if group_id:
        client.masterthesis.groups.update_one(
            {'group': group},
            {
                '$set': {
                    'group': group,
                }
            },
            upsert=True
        )
        return redirect(url_for('group_list'))
    else:
        groups = client.masterthesis.groups.find({})
        return render_template(
            template_name_or_list='groups.html',
            payload={'message': f'No such group {group}', 'groups': groups}
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

    return render_template(
        template_name_or_list='analytics.html',
        typical_users=typical_users
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
