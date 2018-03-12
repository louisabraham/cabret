from collections import namedtuple, deque
import configparser
import os

from . import web

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/config.ini')
for key in ['keys', 'params']:
    if not key in config:
        config[key] = {}

keys = config['keys']


class Proxy(namedtuple('Proxy', 'ip port country anonymity https')):
    @property
    def address(self):
        return '{ip}:{port}'.format(**self._asdict())


class ProxyGetter():

    def get_http_proxy(self):
        raise NotImplementedError

    def get_https_proxy(self):
        while True:
            p = self.get_http_proxy()
            if p.https:
                return p


class ProxyGetter1(ProxyGetter):
    url = 'https://free-proxy-list.net/'

    def __init__(self):
        self.proxies = None
        super().__init__()

    def get_http_proxy(self):
        if self.proxies is None:
            self.proxies = deque(web.get_soup(self.url).tbody)
        self.proxies.rotate(-1)
        p = self.proxies[-1]
        val = [x.text for x in p]
        val[1] = int(val[1])
        val[6] = val[6] == 'yes'
        return Proxy(*val[:3], val[4], val[6])


class ProxyGetter2(ProxyGetter):
    url = 'https://gimmeproxy.com/api/getProxy'
    params = dict(
        api_key=keys.get('gimmeproxy')
    )

    @staticmethod
    def parse_proxy(j):
        return Proxy(
            ip=j['ip'],
            port=int(j['port']),
            country=j['country'],
            anonymity=j['anonymityLevel'],
            https=j['supportsHttps'],
        )

    @classmethod
    def get_http_proxy(cls):
        j = web.json(cls.url, dict(protocol='http', **cls.params))
        return cls.parse_proxy(j)

    @classmethod
    def get_https_proxy(cls):
        j = web.json(cls.url,
                     dict(
                         protocol='http',
                         supportsHttps='true',
                         **cls.params))
        return cls.parse_proxy(j)


class ProxyGetter3(ProxyGetter):
    url = 'http://pubproxy.com/api/proxy'
    params = dict(
        api_key=keys.get('pubproxy')
    )

    @staticmethod
    def parse_proxy(j):
        j = j['data'][0]
        return Proxy(
            ip=j['ip'],
            port=int(j['port']),
            country=j['country'],
            anonymity=j['proxy_level'],
            https=bool(j['support']['https']),
        )

    @classmethod
    def get_http_proxy(cls):
        j = web.json(cls.url, dict(type='http', **cls.params))
        return cls.parse_proxy(j)

    @classmethod
    def get_https_proxy(cls):
        j = web.json(cls.url, dict(
            type='http', https='true', **cls.params))
        return cls.parse_proxy(j)


proxygetterFromName = {
    'free-proxy-list': ProxyGetter1,
    'gimmeproxy': ProxyGetter2,
    'pubproxy': ProxyGetter3,
}

proxyProvider = config['params'].get('proxyProvider', 'free-proxy-list')
proxygetter = proxygetterFromName[proxyProvider]()


get_http_proxy = proxygetter.get_http_proxy
get_https_proxy = proxygetter.get_https_proxy


def get_proxy_for_url(proxy, url):
    if not proxy:
        return None
    if url.startswith('https'):
        if proxy is True:
            proxy = get_https_proxy()
        assert proxy.https, 'Proxy does not support HTTPS but url is HTTPS'
        return {'https': proxy.address}
    elif url.startswith('http'):
        if proxy is True:
            proxy = get_http_proxy()
        return {'http': proxy.address}
    else:
        raise Exception('Unknown URL protocol')
