# Script that authenticates with LinkedIn

import http.cookiejar as cookielib
import os
import urllib
import json
from bs4 import BeautifulSoup
from extractor.linkedin.model.connection import Connection

username = "graham.murr@yahoo.ie"
passphrase = ""
cookie_filename = "parser.cookies.txt"
response_filename = "contacts.json"
contacts_url = "https://www.linkedin.com/connected/api/v1/contacts/connections-only?start=0&count=187&fields=id,name,firstName,lastName,company,title,location,tags,emails,sources,displaySources,connectionDate,secureProfileImageUrl&sort=CREATED_DESC&source=LINKEDIN&_=1481543279665"
connections_url = "https://www.linkedin.com/profile/profile-v2-connections?id=396532726&offset=10&count=20&distance=1&type=SHARED"
connections = []
wait = 1


class LinkedInParser(object):

    def __init__(self, login, password):
        """ Start up... """
        self.login = login
        self.password = password

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
        #self.loginPage()

        title = self.loadTitle()
        print(title)

        # Get contacts to start crawl
        f = open(response_filename, 'w')
        c = self.loadJson(contacts_url)
        f.write(json.dumps(c))

        self.cj.save()

    def loadPage(self, url, data=None):
        """
        Utility function to load HTML from URLs for us with hack to continue despite 404
        """
        # We'll print the url in case of infinite loop
        # print "Loading URL: %s" % url
        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)
            return ''.join([str(l) for l in response.readlines()])
        except Exception as e:
            # If URL doesn't load for ANY reason, try again...
            # Quick and dirty solution for 404 returns because of network problems
            # However, this could infinite loop if there's an actual problem
            print('Load Page Retry')
            return self.loadPage(url, data)

    def loadJson(self, url, data=None):
        """
        Utility function to load HTML from URLs for us with hack to continue despite 404
        """
        # We'll print the url in case of infinite loop
        # print "Loading URL: %s" % url
        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)

            data = response.read()
            encoding = response.info().get_content_charset('utf-8')

            return json.loads(data.decode(encoding))
        except Exception as e:
            # If URL doesn't load for ANY reason, try again...
            # Quick and dirty solution for 404 returns because of network problems
            # However, this could infinite loop if there's an actual problem
            print('Load Page Retry')
            return self.loadPage(url, data)

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

    def parseContacts(self, contacts):
        data = json.load(contacts)
        print(data['values'][0]['name'])


# parser = LinkedInParser(username, passphrase)

raw = open(response_filename)
data = json.load(raw)

for connection in data['values']:

    if connection.get('memberId'):
        member_id = connection['memberId']
        print(member_id)
    else:
        member_id = 0
    print(member_id)

    if connection.get('fullName'):
        name = connection['fullName']
    else:
        name = ""
    print(name)

    if connection.get('title'):
        title = connection['title']
    else:
        title = ""
    print(title)

    if connection.get('company'):
        company = connection['company']['name']
    else:
        company = ""
    print(company)

    if connection.get('graphDistance'):
        distance = connection['graphDistance']
    else:
        distance = ""
    print(distance)

    if connection.get('profileImageUrl'):
        profileImageUrl = connection['profileImageUrl']
    else:
        profileImageUrl = ""
    print(profileImageUrl)

    if connection.get('profileUrl'):
        profileUrl = connection['profileUrl']
    else:
        profileUrl = ""
    print(profileImageUrl)

    connection = Connection(member_id, name, title, company, distance, profileImageUrl, profileUrl)
    connections.append(connection.__dict__)

file = open("connections.json", "w")
file.write(json.dumps(connections))





