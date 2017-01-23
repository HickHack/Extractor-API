# Script that authenticates with LinkedIn

import http.cookiejar as cookielib
import os
import urllib
import json
import jsonpickle
import time
import config as conf
from bs4 import BeautifulSoup
from extractor.linkedin.model.connection import Connection

config = conf.Config().linkedIn()
username = config['username']
passphrase = config['password']
cookie_filename = config['cookie_file']
wait = int(config['request_throttle'])
retry_limit = int(config['retry_limit'])

contacts_url = "https://www.linkedin.com/connected/api/v1/contacts/connections-only?start=%d&count=%d&fields=id,name,firstName,lastName,company,title,location,tags,emails,sources,displaySources,connectionDate,secureProfileImageUrl&sort=CREATED_DESC&source=LINKEDIN"
shared_connections_url = 'https://www.linkedin.com/profile/profile-v2-connections?id=%d&offset=%d&count=%d&distance=1&type=INITIAL'
# = "https://www.linkedin.com/profile/profile-v2-connections?id=%d&offset=%d&count=%d&distance=1&type=SHARED"
limit = 500


class LinkedInParser(object):

    def __init__(self):
        self.login = ''
        self.password = ''
        self.retry_count = 0
        self.pos = 0
        self.total_requests = 0
        self.network = None

    def launch(self, login, password):
        self.login = login
        self.password = password

        # Simulate browser with cookies enabled
        self.cookieJar = cookielib.MozillaCookieJar(cookie_filename)
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

        self.loadRootNode()

        # Get contacts to start crawl
        self.getContacts()

        for connection in self.network[0].connections:
            print(connection.name)
            print("Total Request Made %d" % self.total_requests)

            self.getSharedContacts(connection.member_id)

            if self.pos == limit:
                break

            self.pos += 1

        print("Total Request Made %d" % self.total_requests)

        return self.network

        # TODO: Delete cookies file after crawl

    def loadHtml(self, url, data=None):
        """
        Utility function to load HTML from URLs for us with hack to continue despite 404
        """
        # Throttle Each Request
        time.sleep(wait)
        print ("Loading URL: %s" % url)

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
        soup = BeautifulSoup(open("data/nhome.html"), 'html5lib')

        code = soup.find(id="ozidentity-templates/identity-content")
        content = json.loads(code.contents[0])

        name = content['member']['name']['fullName']
        title = content['member']['headline']['text']
        imageUrl = config['cdn_url'] + content['member']['picture']['id']
        profileUrl = soup.find('ul', {'class': "main-nav"}).findAll('a')[1]['href']

        root = Connection('', name, title, '', 0, imageUrl, profileUrl)
        self.network = [root]

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

    def loadTitle(self):
        soup = self.loadSoup("http://www.linkedin.com/nhome")
        return soup.find("title")

    def getContacts(self):
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

            num_shared = data['content']['connections']['numAll']

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

    @staticmethod
    def mockNetwork():
        network = [Connection]

        with open('/home/graham/code/exograph/extractor/extractor/linkedin/data/connections.json') as data_file:
            data = json.load(data_file)

        for node in data:
            temp = Connection(node['_member_id'], node['_name'], node['_title'], node['_company'],
                              node['_distance'], node['_profileImageUrl'], node['_profileUrl'])

            network.append(temp)
        return network


start_time = int(round(time.time()))
network = LinkedInParser().launch(username, passphrase)
end_time = int(round(time.time()))

print("Total Time Taken: %d seconds" % (end_time - start_time))

file = open("data/test.json", "w")
file.write(jsonpickle.encode(network, unpicklable=False))

