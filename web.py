import gzip

import requests
from bs4 import BeautifulSoup

from . import proxy

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.5',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'}


def urlopen(url, params=None, use_proxy=None):
    return requests.get(url, headers=headers, params=params,
                        proxies=proxy.get_proxy_for_url(use_proxy, url)).text


def json(url, params=None, use_proxy=None):
    return requests.get(url, headers=headers, params=params,
                        proxies=proxy.get_proxy_for_url(use_proxy, url)).json()


def get_soup(url, params=None, use_proxy=None):
    return BeautifulSoup(urlopen(url, params=params,
                                 use_proxy=proxy.get_proxy_for_url(use_proxy, url)),
                         'lxml')

