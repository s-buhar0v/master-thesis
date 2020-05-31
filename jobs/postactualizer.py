import os
import pymongo
from socialmonitor.dataproviders.vk import VkDataExtractor

def _map_vk_post(post):
    return {
        'social_network_id': post['id'],
        'type': 'vk',
        'owner_id': post['owner_id'],
        'group_name': post['group_name'],
        'likes': post['likes']['count'],
        'views': post['views']['count'],
        'comments': post['comments']['count'],
        'reposts': post['reposts']['count'],
    }


def main():
    client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])
    vk_data_extractor = VkDataExtractor()
    db = client.masterthesis
    db_posts = list(db.posts.find({}))

    posts = list(map(lambda _post: f'{_post["owner_id"]}_{_post["social_network_id"]}', db_posts))

    chunked_posts = []
    chunk_size = 100
    for i in range(0, len(posts), chunk_size):
        chunked_posts.append(','.join(posts[i:i + chunk_size]))

    for post in chunked_posts:
        updated_posts = vk_data_extractor.get_posts(post_ids=post)
        for updated_post in updated_posts:
            db.posts.update_one(
                {
                    'social_network_id': updated_post['id'],
                    'owner_id': updated_post['owner_id'],
                },
                {
                    '$set': {
                        'likes': updated_post['likes']['count'],
                        'views': updated_post['views']['count'],
                        'comments': updated_post['comments']['count'],
                        'reposts': updated_post['reposts']['count'],
                    }
                },
                upsert=False
            )


if __name__ == '__main__':
    main()
