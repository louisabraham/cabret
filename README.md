cabret
======

Various utilities for making bots.

<img src="http://ffden-2.phys.uaf.edu/webproj/212_spring_2015/Katrina_Howe/Howe_Katrina/Pictures%20for%20Web%20Proj/Hugo1.JPG"
title="The automaton from the book The Invention of Hugo Cabret" width="20%"/>

Web scraping
------------

Just a basic wrapper around
[requests](http://docs.python-requests.org/en/master/) with a default
user-agent and that supports auto-discovered proxies. Can return raw
html,
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
or json.

``` pycon
>>> from cabret import web
>>> web.json('http://echo.jsontest.com/key/value/one/two')
{'one': 'two', 'key': 'value'}
```

Proxy discovery
---------------

We provide simple functions to get proxies from the following websites:

-   https://free-proxy-list.net/
-   http://pubproxy.com/
-   https://gimmeproxy.com/

Those are great websites, it is encouraged to get a premium account. If
you have an API key for pubproxy or gimmeproxy, you can put it in your
configuration file.

``` pycon
>>> from cabret import proxy
>>> proxy.get_https_proxy()
Proxy(ip='191.251.165.63', port=8080, country='BR', anonymity='elite proxy', https=True)
>>> from cabret import web
>>> web.urlopen('https://ifconfig.co/ip', use_proxy=True)
'2a03:4000:21:435::dead:beef\n'
```

By default, https://free-proxy-list.net/ is used. You can change that in
`config.ini`.

Get validation emails
---------------------

For the moment, we support only https://mailsac.com/.

``` pycon
>>> from cabret.email import mailsac as ms
>>> ms.full_address('address')
EmailAddress(address@mailsac.com)
>>> msg = ms.message_list('address')[0]
>>> ms.get_message_text(msg)
'cabret is awesome!'
>>> msg['from']
[{'name': '', 'address': 'example@example.com'}]
```

Mailsac is really great, you should get a premium account to support
them (although you can do almost everything for free)!

You can put your API key in `config.ini`.

Scrape some websites
--------------------

### Reddit

``` pycon
>>> from cabret import web
>>> from cabret.scrapers import reddit
>>> posts = next(reddit.gen_posts('https://www.reddit.com/r/copypasta'))
>>> len(posts) # posts on the first page
26
>>> posts[0]
Post(title='Today r/copypasta is joining Operation: #OneMoreVote to save net neutrality', domain='self.copypasta', url='https://www.reddit.com/r/copypasta/comments/80pfhp/today_rcopypasta_is_joining_operation_onemorevote/', comments='https://www.reddit.com/r/copypasta/comments/80pfhp/today_rcopypasta_is_joining_operation_onemorevote/', author='SMUT_ADDICT', subreddit='copypasta')
>>> reddit.get_post_text(posts[0])
'This past December, the FCC voted to kill net neutrality, letting internet providers like Verizon and Comcast impose new fees, throttle bandwidth, and censor online content. If this happens, subreddits like this one might not exist.\nWe can still block the repeal using the Congressional Review Act (CRA), and we’re just one vote away from winning in the Senate and taking the fight to the House. That’s why today we’re joining Operation: #OneMoreVote, an Internet-wide day of action.\nThis affects every redditor as well as every Internet user, and we only have a 60 legislative days left to stop it. Please, take a moment of your time to join the protest by contacting your lawmakers.\n'
```

The module is also a commandline utility. To scrape the text from the
posts of the 3 first pages of /r/copypasta/ with parallel downloading:

``` bash
python3 -m cabret.scrapers.reddit 3 /r/copypasta/
```

Configuration
-------------

You can add a configuration file under `config.ini`, following the
instruction in `example-config.ini`.
