import configparser
import os

from . import web

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/config.ini')
for key in ['keys', 'params']:
    if not key in config:
        config[key] = {}

keys = config['keys']


class EmailAddress():
    def __init__(self, *args):
        if len(args) == 1:
            self.username, self.domain = args[0].split('@')
        else:
            assert len(args) == 2
            self.username, self.domain = args

    @property
    def address(self):
        return '%s@%s' % (self.username, self.domain)
    
    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.address)


class MailHandler():

    def full_address(self, username):
        return EmailAddress(username, self.domain)

    def username(self, address):
        if isinstance(address, EmailAddress):
            return address.username
        return address.split('@')[0]


class Mailsac(MailHandler):
    url = 'https://mailsac.com/api'
    domain = 'mailsac.com'

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.params = dict(
            _mailsacKey=api_key
        )

    def message_list(self, address):
        address = self.username(address)
        url = '%s/addresses/%s@mailsac.com/messages' % (self.url, address)
        return web.json(url, params=self.params)

    def get_message(self, address, id):
        "Retrieve message from id"
        address = self.username(address)
        if self.api_key is None:
            raise Exception('Needs API key')
        url = '%s/addresses/%s@mailsac.com/messages/%s' % (
            self.url, address, id)
        return web.json(url, params=self.params)

    def get_message_text(self, msg):
        address = self.username(msg['originalInbox'])
        id = self.get_message_id(msg)
        url = '%s/text/%s@mailsac.com/%s' % (self.url, address, id)
        return web.urlopen(url, params=self.params)

    def get_message_links(self, msg):
        return msg['links']

    def get_message_id(self, msg):
        return msg['_id']


mailsac = Mailsac(keys.get('mailsac'))
