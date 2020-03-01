import os
import pymongo

group_name = 'w220.club'


def main():
    client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])
    db = client.masterthesis
    posts = list(db.posts.find({'group_name': group_name}))
    metrics = db.metrics

    base_metrics = {
        'likes': list(map(lambda _post: _post['likes'], posts)),
        'comments': list(map(lambda _post: _post['comments'], posts)),
        'reposts': list(map(lambda _post: _post['reposts'], posts)),
        'views': list(map(lambda _post: _post['views'], posts))
    }

    for metric in base_metrics:
        metrics.update_one(
            {
                'metrics': metric,
                'group': group_name
            },
            {
                '$set': {
                    'metrics': metric,
                    'group': group_name,
                    'value': sum(base_metrics[metric])
                },
            },
            upsert=True
        )


if __name__ == '__main__':
    main()
