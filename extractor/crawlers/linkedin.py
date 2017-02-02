"""
LinkedIn crawler for pulling connection data from the LinkedIn api
"""

import http.cookiejar as cookielib
import json
import os
import time
import urllib

from json.decoder import JSONDecodeError
import networkx as nx
from bs4 import BeautifulSoup
from random import randint

import extractor.config as conf
from extractor.model.linkedin import Connection

config = conf.Config().linkedIn()
cookie_filename = config['cookie_file']
wait = int(config['request_throttle'])
retry_limit = int(config['retry_limit'])

contacts_url = config['contacts_url']
all_connections_url = config['all_connections_url']
shared_connections_url = config['shared_connections_url']


class LinkedInCrawler(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.retry_count = 0
        self.pos = 0
        self.total_requests = 0
        self.network = None
        self.cookie_jar = cookielib.MozillaCookieJar(os.path.dirname(os.path.realpath(__file__)) + cookie_filename)
        self.opener = None
        self.G = Graph()
        self.root_id = 0

    def launch(self):
        # Simulate browser
        self.configure_opener()

        try:
            self.login()
            self.load_seed()
            self.load_contacts()
        except Exception as e:
            return e

        # Start fetching all shared contacts
        for connection in self.network[0].connections:
            print('%s\nTotal Request Made %d' % (connection.name, self.total_requests))

            self.load_shared_connections(connection.member_id)
            self.pos += 1

        self.G.write_to_file()
        return self.G.get_graph(), self.root_id

        # TODO: Delete cookies file after crawl

    def configure_opener(self):
        if os.access(cookie_filename, os.F_OK):
            self.cookie_jar.load()

        self.opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(debuglevel=0),
            urllib.request.HTTPSHandler(debuglevel=0),
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )

        self.opener.addheaders = [
            ('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)')
        ]

    def request_html(self, url, data=None):

        response = self.request(url, data)
        if response is not None:
            return ''.join([str(l) for l in response.readlines()])
        else:
            return ''

    def request_json(self, url, data=None):

        response = self.request(url, data)
        body = response.read()
        encoding = response.info().get_content_charset('utf-8')

        try:
            return json.loads(body.decode(encoding))
        except JSONDecodeError as e:
            return {}

    def request(self, url, data=None):
        print("Loading URL: %s" % url)

        # Throttle Each Request
        time.sleep(wait)

        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)
            self.total_requests += 1

            return response
        except Exception as e:
            # If URL doesn't load for ANY reason, try again...
            print("Retry %d" % self.retry_count)

            if self.retry_count <= retry_limit:
                self.retry_count += 1
                return self.request(url, data)
            else:
                self.retry_count = 0
                return None

    """
    Combine loading of URL, HTML, and parsing with BeautifulSoup
    """

    def load_soup(self, url, data=None):
        html = self.request_html(url, data)
        soup = BeautifulSoup(html, "html5lib")

        return soup

    """
    Fetches the root node which the account of root node
    """
    def load_seed(self):
        soup = self.load_soup("http://www.linkedin.com/nhome")
        profile_data = soup.find(id="ozidentity-templates/identity-content")
        member_id_data = soup.find(id="sharebox-static/templates/share-content")

        try:
            content = json.loads(profile_data.contents[0])
            member_id_content = json.loads(member_id_data.contents[0])
        except Exception:
            raise NoDataException('No seed data found')

        try:
            self.root_id = int(member_id_content['memberInfo']['id']) if 'id' in member_id_content['memberInfo'] else randint(0, 8000)
            name = content['member']['name']['fullName'] if 'fullName' in content['member']['name'] else ' '
            title = content['member']['headline']['text'] if 'text' in content['member']['headline'] else ' '
            profile_image_url = config['cdn_url'] + content['member']['picture']['id'] if 'id' in content['member']['picture'] else ' '

            url = soup.find('ul', {'class': "main-nav"}).findAll('a')[1]['href']
            profile_url = url if url is not None else ' '

        except KeyError:
            raise ParseException('Error Parsing Seed')

        root = Connection(self.root_id, name, title,
                          ' ', ' ', ' ',
                          ' ', ' ', ' ',
                          profile_image_url, profile_url, True)

        self.network = [root]
        self.G.add_node(root.name, root.__dict__)

    """
    Handle login. This should populate our cookie jar.
    """

    def login(self):
        soup = self.load_soup("https://www.linkedin.com/")
        csrf = soup.find(id="loginCsrfParam-login")['value']
        login_data = urllib.parse.urlencode({
            'session_key': self.username,
            'session_password': self.password,
            'loginCsrfParam': csrf,
        }).encode('utf8')

        response = self.request("https://www.linkedin.com/uas/login-submit", login_data)

        if response.url != config['home_url']:
            raise LoginException('Login Failed')

        self.cookie_jar.save()

    def load_contacts(self):
        count = 10
        start = 0

        # Make initial request for 10 items
        data = self.request_json(contacts_url % (start, count))

        if ('values' not in data) or ('paging' not in data):
            raise ParseException('No data to start crawl')

        total = data['paging']['total']

        if total <= 200:
            # Request all in one swoop
            data = self.request_json(contacts_url % (start, total))
            self.parse_contacts(data)
        else:
            # TODO: Add Paging
            print('')

    def load_shared_connections(self, member_id):
        count = 10
        offset = 0

        # TODO: Handle case when user has premium account (Martin Duffy)

        # Make initial request for 10 items
        data = self.request_json(shared_connections_url % (member_id, offset, count))

        if data is not None and self.has_shared_connections(data):
            self.parse_shared_connections(data)
            total = len(self.network[0].connections[self.pos].connections)

            num_shared = data['content']['connections']['numShared']

            if num_shared > 10:
                while offset < num_shared and total < num_shared:
                    offset += 10
                    data = self.request_json(shared_connections_url % (member_id, offset, count))

                    if data is not None and self.has_shared_connections(data):
                        self.parse_shared_connections(data)
                    total = len(self.network[0].connections[self.pos].connections)

    @staticmethod
    def has_shared_connections(data):
        if not data['content']['connections']:
            return False
        return True

    def parse_contacts(self, contacts):
        if contacts['values']:
            for connection in contacts['values']:
                node = Connection.parse_contact(connection)

                self.network[0].addConnection(node)

                # Add non existent node and add edge from root -> connection
                self.G.add_node(node.name, node.__dict__)
                self.G.add_edge(self.network[0].name, node.name)

    def parse_shared_connections(self, shared):
        for connection in shared['content']['connections']['connections']:
            node = Connection.parse_shared_connection(connection)

            self.network[0].connections[self.pos].addConnection(node)
            self.G.add_edge(self.network[0].connections[self.pos].name, node.name)

    @staticmethod
    def mock_network():
        file = os.path.dirname(os.path.realpath(__file__)) + '/data/linkedin.graphml'

        if os.access(file, os.F_OK):
            return nx.read_graphml(file)


class Graph(object):
    def __init__(self):
        self._G = nx.Graph()

    # Add (key, attribute dict)
    def add_node(self, k, attr_dict):
        clean_attr = self.clean_attr(attr_dict)
        self._G.add_node(k, clean_attr)

    # Add edge from n -> v
    def add_edge(self, n, v):
        self._G.add_edge(n, v)

    # Returns true is exists
    def does_node_exist(self, n):
        return n in self._G.nodes()

    def write_to_file(self):
        nx.write_graphml(self._G, os.path.dirname(os.path.realpath(__file__)) + '/data/linkedin.graphml')

    def get_graph(self):
        return self._G

    @staticmethod
    def clean_attr(attr_dict):
        props = dict(attr_dict)

        if 'connections' in props:
            del props['connections']
        return props


class LoginException(Exception):
    def __init__(self, message):
        super(LoginException, self).__init__(message)


class ParseException(Exception):
    def __init__(self, message):
        super(ParseException, self).__init__(message)


class NoDataException(Exception):
    def __init__(self, message):
        super(NoDataException, self).__init__(message)



