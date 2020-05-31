import os
import pymongo
from socialmonitor.dataproviders.vk import VkDataExtractor

vk_data_extractor = VkDataExtractor()


def _is_user_accessible(user):
    if 'deactivated' in user:
        return False
    if 'is_closed' in user:
        return not user['is_closed']


def _get_group_members_ids(group_name):
    chunk_size = 1000

    all_members = []
    members_count = vk_data_extractor.get_group_members_count(group_name=group_name)

    for i in range(0, members_count, chunk_size):
        all_members.extend(vk_data_extractor.get_group_members_ids(group_name=group_name, offset=i))

    active_members = list(filter(_is_user_accessible, all_members))
    active_members_ids = list(map(lambda _member: _member['id'], active_members))

    return {
        'members': active_members_ids,
        'count': len(active_members)
    }


def main():
    client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])
    db = client.masterthesis
    groups = db.groups.find({})

    for g in groups:
        active_group_members_ids = _get_group_members_ids(group_name=g['group'])
        existing_group_members_ids = set(db.users.distinct('id'))

        new_members_ids = list(set(active_group_members_ids['members']) - existing_group_members_ids)
        new_members = []

        if new_members_ids:
            for i in range(0, len(new_members_ids), 300):
                user_ids = ','.join(map(str, new_members_ids[i:i + 300]))
                new_members.extend(
                    vk_data_extractor.get_users(
                        user_ids=user_ids,
                        group_name=g['group']
                    )
                )

        if new_members:
            db.users.insert_many(new_members)


if __name__ == '__main__':
    main()
