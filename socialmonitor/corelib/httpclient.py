import requests


class HttpClientMixin(object):
    def __init__(self, api_base_url):
        self._api_base_url = api_base_url
        self._method_map = {
            'get': self._get
        }

    def request(self, **kwargs):
        kwargs.setdefault('headers', {}).update({
            'Content-Type': 'application/json'
        })

        if 'method' in kwargs:
            method = kwargs.pop('method')
        else:
            raise KeyError('No method provided')

        if 'endpoint' in kwargs:
            endpoint = kwargs.pop('endpoint')
        else:
            raise KeyError('No endpoint provided')

        if method in self._method_map:
            return self._method_map[method](endpoint=endpoint, **kwargs)
        else:
            raise ValueError('Unsupported method')

    def _get(self, endpoint, **kwargs):
        return requests.get(url=f'{self._api_base_url}{endpoint}', **kwargs)


