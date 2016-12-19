# Script that authenticates with LinkedIn

import http.cookiejar as cookielib
import os
import urllib
import json
import time
from bs4 import BeautifulSoup
from extractor.linkedin.model.connection import Connection

username = "graham.murr@yahoo.ie"
passphrase = "Pa55w0rd!"
cookie_filename = "parser.cookies.txt"
contacts_filename = "contacts.json"
shared_contacts_filename = "share.contacts.json"
contacts_url = "https://www.linkedin.com/connected/api/v1/contacts/connections-only?start=%d&count=%d&fields=id,name,firstName,lastName,company,title,location,tags,emails,sources,displaySources,connectionDate,secureProfileImageUrl&sort=CREATED_DESC&source=LINKEDIN"
connections_url = "https://www.linkedin.com/profile/profile-v2-connections?id=%d&offset=%d&count=%d&distance=1&type=SHARED"
connections = []
wait = 0
retry_limit = 3


class LinkedInParser(object):

    def __init__(self, login, password):
        """ Start up... """
        self.login = login
        self.password = password
        self.retry_count = 0
        self.pos = 0
        self.total_requests = 0

        # Simulate browser with cookies enabled
        self.cj = cookielib.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(debuglevel=0),
            urllib.request.HTTPSHandler(debuglevel=0),
            urllib.request.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)')
        ]

        # Login
        self.loginPage()
        self.cj.save()

        title = self.loadTitle()
        print(title)

        # Get contacts to start crawl
        self.getContacts()
        for connection in connections:
            print(connection.name)
            print("Total Request Made %d" % self.total_requests)

            self.getSharedContacts(connection.member_id)
            self.pos += 1

        print("Total Request Made %d" % self.total_requests)

    def loadPage(self, url, data=None):
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
            return self.loadPage(url, data)

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

            print('JSON Retry ' + self.retry_count)

            if self.retry_count <= retry_limit:
                self.retry_count += 1
                return self.loadJson(url, data)
            else:
                raise Exception('Unable to Load JSON')

    def loadSoup(self, url, data=None):
        """
        Combine loading of URL, HTML, and parsing with BeautifulSoup
        """
        html = self.loadPage(url, data)
        soup = BeautifulSoup(html, "html5lib")
        return soup

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

        self.loadPage("https://www.linkedin.com/uas/login-submit", login_data)
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
            print("Start Paging")

    def getSharedContacts(self, member_id):
        count = 10
        offset = 0

        # Make initial request for 10 items
        data = self.loadJson(connections_url % (member_id, offset, count))

        if self.hasSharedConnections(data):
            self.parseSharedConnections(data)
            total = len(connections[self.pos].sharedConnections)

            num_shared = data['content']['connections']['numShared']

            if num_shared > 10:
                while offset < num_shared and total < num_shared:
                    offset += 10
                    data = self.loadJson(connections_url % (member_id, offset, count))
                    if self.hasSharedConnections(data):
                        self.parseSharedConnections(data)
                    total = len(connections[self.pos].sharedConnections)

    @staticmethod
    def hasSharedConnections(data):
        if not data['content']['connections']:
            return False

        return True

    @staticmethod
    def parseContacts(contacts):
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
                connections.append(connection)
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
            connections[self.pos].addConnection(tmp)


start_time = int(round(time.time()))
parser = LinkedInParser(username, passphrase)
end_time = int(round(time.time()))

print("Total Time Taken: %d seconds" % (end_time - start_time))

connections_dict = []
for node in connections:
    tmp_dict = []

    for tmp_shared in node.sharedConnections:
        tmp_dict.append(tmp_shared.__dict__)

    node._sharedConnections = tmp_dict
    tmp_dict = []

    connections_dict.append(node.__dict__)

file = open("connections.json", "w")
file.write(json.dumps(connections_dict))

