#!/usr/bin/env python3

"""
Scrapes the texts of the n first pages starting from
the url and print the ones with only ASCII characters

n is the first command line argument
if n is -1, continues until there is a 'next' link

url is the second argument and defaults to
https://www.reddit.com/r/copypasta/top/?sort=top&t=all
"""

import urllib.parse
import sys
from collections import namedtuple

from .. import web
from ..utils import parallel_map, tqdm

Post = namedtuple('Post', 'title domain url comments author subreddit')

def get_reddit_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://www.reddit.com' + urllib.parse.quote(url)
    return url

def get_posts_from_soup(soup):
    """
    List of all posts from a page
    """
    elements = list(soup.find('div', {'id': 'siteTable'}))
    ans = []
    for e in elements[:-1:2]:
        titleElement = e.find(class_='title')
        title = titleElement.a.text
        url = get_reddit_url(titleElement.a.get('href'))
        domain = e.find(class_='domain').a.text
        comments = e.li.a.get('href')
        author = e.get('data-author')
        subreddit = e.get('data-subreddit')
        post = Post(title, domain, url, comments, author, subreddit)
        ans.append(post)
    nexturl = elements[-1].find('a', {'rel': 'nofollow next'})
    if nexturl is not None:
        nexturl = nexturl.get('href')
    return ans, nexturl


def gen_posts(url, nb_pages=None, use_tqdm=True):
    for _ in tqdm(nb_pages, cond=use_tqdm):
        posts, url = get_posts_from_soup(web.get_soup(url))
        yield posts
        if url is None:
            break
    return url

def get_post_text(url):
    if isinstance(url, Post):
        url = url.url
    if not url.startswith('https://www.reddit.com/'):
        return ''
    soup = web.get_soup(url)
    elements = soup.select('#siteTable')[0]
    md = elements.find(class_='md')
    if md is None:
        return ''
    ans = md.text
    assert ans.endswith('\n')
    return ans

def gen_text(url, nb_pages=None, use_tqdm=True,
             batch=25, post_filter=bool, text_filter=bool):
    for posts in gen_posts(url, nb_pages, use_tqdm=use_tqdm):
        urls = [p.url for p in filter(post_filter, posts)]
        contents = parallel_map(get_post_text, urls)
        yield from filter(text_filter, contents)


def ASCII_filter(p):
    return p and all(ord(c) < 128 for c in p)


is_main = __name__ == '__main__'

if is_main:

    nb_pages = int(sys.argv[1])
    url = get_reddit_url(sys.argv[2]) if len(sys.argv) > 2 else 'https://www.reddit.com/'
    for t in gen_text(url, nb_pages,
                      text_filter=ASCII_filter):
        print(t)
