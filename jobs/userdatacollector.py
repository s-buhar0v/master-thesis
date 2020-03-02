import os
import pymongo
from socialmonitor.dataproviders.vk import VkDataExtractor

group_name = 'w220.club'


def _is_user_accessible(user):
    if 'deactivated' in user:
        return False
    if 'is_closed' in user:
        return not user['is_closed']


def main():
    client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])
    db = client.masterthesis
    vk_data_extractor = VkDataExtractor()
    chunk_size = 1000
    mongo_chunk_size = 10000

    members = []

    members_count = vk_data_extractor.get_group_members_count(group_name=group_name)

    for i in range(0, members_count, chunk_size):
        members.extend(vk_data_extractor.get_group_members(group_name=group_name, offset=i))

    filtered_members = list(filter(_is_user_accessible, members))

    db.users.insert_many(filtered_members)


if __name__ == '__main__':
    main()
