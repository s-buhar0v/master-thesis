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
            'v': '5.92'
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

    def get_group_members_count(self, group_name):
        params = {
            'group_id': group_name,
            'count': 0
        }

        params.update(self._default_params)

        return self.request(method='get', endpoint='/groups.getMembers', params=params).json()['response']['count']

