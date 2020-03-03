import os

from socialmonitor.corelib.httpclient import HttpClientMixin


class VkDataExtractor(HttpClientMixin):
    def __init__(self):
        HttpClientMixin.__init__(
            self,
            api_base_url='https://api.vk.com/method'
        )
        self._default_params = {
            'access_token': os.environ['VK_API_ACCESS_TOKEN'],
            'v': '5.103'
        }

    def get_group_posts_count(self, group_name):
        params = {
            'domain': group_name,
            'count': 0,
            'extended': 0
        }
        params.update(self._default_params)

        return self.request(method='get', endpoint='/wall.get', params=params).json()['response']['count']

    def get_group_posts(self, group_name, count=2):
        params = {
            'domain': group_name,
            'count': count,
            'extended': 1
        }
        params.update(self._default_params)

        return self.request(method='get', endpoint='/wall.get', params=params).json()['response']['items']

    def get_posts(self, post_ids):
        params = {
            'posts': post_ids,
            'extended': 1
        }
        params.update(self._default_params)

        return self.request(method='get', endpoint='/wall.getById', params=params).json()['response']['items']

    def get_group_members_count(self, group_name):
        params = {
            'group_id': group_name,
            'count': 0
        }

        params.update(self._default_params)

        return self.request(method='get', endpoint='/groups.getMembers', params=params).json()['response']['count']

    def get_group_members_ids(self, group_name, count=1000, offset=0):
        params = {
            'fields': 'deactivated,is_closed',
            'group_id': group_name,
            'count': count,
            'offset': offset
        }

        params.update(self._default_params)

        return self.request(method='get', endpoint='/groups.getMembers', params=params).json()['response']['items']

    def get_users(self, user_ids):
        params = {
            'user_ids': user_ids,
            'fields': 'sex,bdate,city,country,photo_max_orig,domain,connections,universities,last_seen,relation,music,personal,movies',
        }

        params.update(self._default_params)

        return self.request(method='get', endpoint='/users.get', params=params).json()['response']
