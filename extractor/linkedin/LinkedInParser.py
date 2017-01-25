# Script that authenticates with LinkedIn

import http.cookiejar as cookielib
import json
import os
import time
import urllib
import jsonpickle
import extractor.config as conf
import networkx as nx
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from extractor.linkedin.model.connection import Connection

config = conf.Config().linkedIn()
username = config['username']
passphrase = config['password']
cookie_filename = config['cookie_file']
wait = int(config['request_throttle'])
retry_limit = int(config['retry_limit'])

contacts_url = "https://www.linkedin.com/connected/api/v1/contacts/connections-only?start=%d&count=%d&fields=id,name,firstName,lastName,company,title,location,tags,emails,sources,displaySources,connectionDate,secureProfileImageUrl&sort=CREATED_DESC&source=LINKEDIN"
all_connections_url = 'https://www.linkedin.com/profile/profile-v2-connections?id=%d&offset=%d&count=%d&distance=1&type=INITIAL'
shared_connections_url = "https://www.linkedin.com/profile/profile-v2-connections?id=%d&offset=%d&count=%d&distance=1&type=SHARED"


class LinkedInParser(object):

    def __init__(self):
        self.login = ''
        self.password = ''
        self.retry_count = 0
        self.pos = 0
        self.total_requests = 0
        self.network = None
        self.G = Graph()

    def launch(self, login, password):
        self.login = login
        self.password = password

        # Simulate browser with cookies enabled
        self.cookieJar = cookielib.MozillaCookieJar(os.path.dirname(os.path.realpath(__file__)) + cookie_filename)

        if os.access(cookie_filename, os.F_OK):
            self.cookieJar.load()

        self.opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(debuglevel=0),
            urllib.request.HTTPSHandler(debuglevel=0),
            urllib.request.HTTPCookieProcessor(self.cookieJar)
        )

        self.opener.addheaders = [
            ('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)')
        ]

        # Login
        self.loginPage()
        self.cookieJar.save()

        # Get contacts to start crawl
        self.loadRootNode()
        self.loadContacts()

        # Start fetching all shared contacts
        for connection in self.network[0].connections:
            print(connection.name)
            print("Total Request Made %d" % self.total_requests)

            self.getSharedContacts(connection.member_id)

            self.pos += 1

        print("Total Request Made %d" % self.total_requests)

        return self.G

        # TODO: Delete cookies file after crawl

    def loadHtml(self, url, data=None):
        """
        Utility function to load HTML from URLs for us with hack to continue despite 404
        """
        # Throttle Each Request
        time.sleep(wait)
        print("Loading URL: %s" % url)

        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)

            self.total_requests += 1
            return ''.join([str(l) for l in response.readlines()])
        except Exception as e:
            # If URL doesn't load for ANY reason, try again...
            # Quick and dirty solution for 404 returns because of network problems
            # However, this could infinite loop if there's an actual problem
            # TODO: add timeout
            print('Load Page Retry')
            return self.loadHtml(url, data)

    def loadJson(self, url, data=None):
        """
        Utility function to load JSON
        """
        # Throttle Each Request
        time.sleep(wait)
        print("Loading URL: %s" % url)

        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)

            self.total_requests += 1
            data = response.read()
            encoding = response.info().get_content_charset('utf-8')

            return json.loads(data.decode(encoding))
        except Exception as e:
            # If URL doesn't load for ANY reason, try again...
            print("Retry %d" % self.retry_count)

            if self.retry_count <= retry_limit:
                self.retry_count += 1
                return self.loadJson(url, data)
            else:
                print('Retry Limit Reached')
                return None

    def loadSoup(self, url, data=None):
        """
        Combine loading of URL, HTML, and parsing with BeautifulSoup
        """
        html = self.loadHtml(url, data)
        soup = BeautifulSoup(html, "html5lib")

        return soup

    def loadRootNode(self):
        soup = self.loadSoup("http://www.linkedin.com/nhome")

        code = soup.find(id="ozidentity-templates/identity-content")
        content = json.loads(code.contents[0])

        name = content['member']['name']['fullName']
        title = content['member']['headline']['text']
        imageUrl = config['cdn_url'] + content['member']['picture']['id']
        profileUrl = soup.find('ul', {'class': "main-nav"}).findAll('a')[1]['href']

        root = Connection('R', name, title, '', 0, imageUrl, profileUrl)
        self.network = [root]
        self.G.add_node(root.name, root.__dict__)

    def loginPage(self):
        """
        Handle login. This should populate our cookie jar.
        """
        soup = self.loadSoup("https://www.linkedin.com/")
        csrf = soup.find(id="loginCsrfParam-login")['value']
        login_data = urllib.parse.urlencode({
            'session_key': self.login,
            'session_password': self.password,
            'loginCsrfParam': csrf,
        }).encode('utf8')

        self.loadHtml("https://www.linkedin.com/uas/login-submit", login_data)
        return

    def loadContacts(self):
        count = 10
        start = 0

        # Make initial request for 10 items
        data = self.loadJson(contacts_url % (start, count))

        if not data['values']:
            raise Exception("No Data Found")
        elif not data['paging']:
            raise Exception("No Paging Data Found")

        total = data['paging']['total']

        if total <= 200:
            # Request all in one swoop
            data = self.loadJson(contacts_url % (start, total))
            self.parseContacts(data)
        else:
            # TODO: Add Paging
            print("Start Paging")

    def getSharedContacts(self, member_id):
        count = 10
        offset = 0

        # TODO: Handle case when user has premium account (Martin Duffy)

        # Make initial request for 10 items
        data = self.loadJson(shared_connections_url % (member_id, offset, count))

        if data is not None and self.hasSharedConnections(data):
            self.parseSharedConnections(data)
            total = len(self.network[0].connections[self.pos].connections)

            num_shared = data['content']['connections']['numShared']

            if num_shared > 10:
                while offset < num_shared and total < num_shared:
                    offset += 10
                    data = self.loadJson(shared_connections_url % (member_id, offset, count))

                    if data is not None and self.hasSharedConnections(data):
                        self.parseSharedConnections(data)
                    total = len(self.network[0].connections[self.pos].connections)

    @staticmethod
    def hasSharedConnections(data):
        if not data['content']['connections']:
            return False
        return True

    def parseContacts(self, contacts):
        if contacts['values']:
            for connection in contacts['values']:

                if connection.get('memberId'):
                    member_id = connection['memberId']
                else:
                    member_id = 0

                if connection.get('fullName'):
                    name = connection['fullName']
                else:
                    name = ""

                if connection.get('title'):
                    title = connection['title']
                else:
                    title = ""

                if connection.get('company'):
                    company = connection['company']['name']
                else:
                    company = ""

                if connection.get('graphDistance'):
                    distance = connection['graphDistance']
                else:
                    distance = ""

                if connection.get('profileImageUrl'):
                    profileImageUrl = connection['profileImageUrl']
                else:
                    profileImageUrl = ""

                if connection.get('profileUrl'):
                    profileUrl = connection['profileUrl']
                else:
                    profileUrl = ""

                connection = Connection(member_id, name, title, company, distance, profileImageUrl, profileUrl)

                self.network[0].addConnection(connection)

                # Add non existent node and add edge from root -> connection
                self.G.add_node(connection.name, connection.__dict__)
                self.G.add_edge(self.network[0].name, connection.name)
        else:
            raise Exception("No Data Found")

    def parseSharedConnections(self, shared):
        for connection in shared['content']['connections']['connections']:

            if connection.get('memberID'):
                member_id = connection['memberID']
            else:
                member_id = 0

            if connection.get('fmt__full_name'):
                name = connection['fmt__full_name']
            else:
                name = ""

            if connection.get('headline'):
                title = connection['headline']
            else:
                title = ""

            if connection.get('distance'):
                distance = connection['distance']
            else:
                distance = 0

            if connection.get('mem_pic'):
                profileImageUrl = connection['mem_pic']
            else:
                profileImageUrl = ""

            if connection.get('pview'):
                profileUrl = connection['pview']
            else:
                profileUrl = ""

            tmp = Connection(member_id, name, title, "", distance, profileImageUrl, profileUrl)

            self.network[0].connections[self.pos].addConnection(tmp)
            self.G.add_edge(self.network[0].connections[self.pos].name, tmp.name)

    @staticmethod
    def mockNetwork():

        with open(os.path.dirname(os.path.realpath(__file__)) + '/data/test.json') as data_file:
            data = data_file.read().replace('\n', '')
            return jsonpickle.decode(data)


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

    def getGraph(self):
        return self._G

    def draw(self):
        graph_pos = nx.spring_layout(self._G)

        # draw nodes, edges and labels
        # nx.draw_networkx_nodes(self._G, graph_pos, node_size=1000, node_color='blue', alpha=0.3)
        # nx.draw_networkx_edges(self._G, graph_pos)
        # nx.draw_networkx_labels(self._G, graph_pos, font_size=12, font_family='sans-serif')

        nx.draw(self._G, graph_pos, node_color='#A0CBE2', edge_color='#B0C23E', width=2, edge_cmap=plt.cm.Blues,
                with_labels=True)
        plt.show()

    def write_to_file(self):
        # TODO add dynamic file path
        nx.write_graphml(self._G, "/home/graham/code/exograph/extractor_api/extractor/linkedin/data/linkedin.graphml")

    @staticmethod
    def clean_attr(attr_dict):
        props = dict(attr_dict)

        if 'connections' in props:
            del props['connections']
        return props

start_time = int(round(time.time()))
graph = LinkedInParser().launch(username, passphrase)
end_time = int(round(time.time()))

print("Total Time Taken: %d seconds" % (end_time - start_time))

graph.write_to_file()



