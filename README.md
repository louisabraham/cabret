cabret
======

Various utilities for making bots.

<img src="http://ffden-2.phys.uaf.edu/webproj/212_spring_2015/Katrina_Howe/Howe_Katrina/Pictures%20for%20Web%20Proj/Hugo1.JPG"
title="The automaton from the book The Invention of Hugo Cabret" width="20%"/>

Web scraping
------------

Just a base wrapper around requests with a default user-agent and that
supports proxies. Can return raw html, BeautifulSoup or json.

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
>>> from cabret import web
>>> web.urlopen('https://ifconfig.co/ip', use_proxy=True)
'2a03:4000:21:435::dead:beef\n'
```

By default, https://free-proxy-list.net/ is used. You can change that
with `config.ini`.

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
them!

You can put your API key in `config.ini`.

Configuration
-------------

You can add a configuration file under `config.ini`, following the
instruction in `example-config.ini`.
