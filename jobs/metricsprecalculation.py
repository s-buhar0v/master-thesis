import os
import pymongo



def main():
    client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])
    db = client.masterthesis
    groups = db.groups.find({})

    for g in groups:
        posts = list(db.posts.find({'group_name': g['group']}))
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
                    'group': g['group']
                },
                {
                    '$set': {
                        'metrics': metric,
                        'group': g['group'],
                        'value': sum(base_metrics[metric])
                    },
                },
                upsert=True
            )


if __name__ == '__main__':
    main()
