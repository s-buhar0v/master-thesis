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
    db = client.masterthesis
    posts = db.posts
    groups = db.groups.find({})

    vk_data_extractor = VkDataExtractor()

    for g in groups:
        vk_group_posts = vk_data_extractor.get_group_posts(group_name=g['group'])
        vk_group_mapped_posts = list(map(_map_vk_post, vk_group_posts))

        for post in vk_group_mapped_posts:
            existing_post = posts.find_one({'social_network_id': post['social_network_id']})

            if not existing_post:
                posts.insert_one(post)


if __name__ == '__main__':
    main()
