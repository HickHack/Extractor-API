# Script that authenticates with LinkedIn

import http.cookiejar as cookielib
import os
import urllib
import json
from bs4 import BeautifulSoup

username = "graham.murr@yahoo.ie"
passphrase = ""
cookie_filename = "parser.cookies.txt"
response_filename = "contacts.json"
contacts_url = "https://www.linkedin.com/connected/api/v1/contacts/connections-only?start=0&count=187&fields=id,name,firstName,lastName,company,title,location,tags,emails,sources,displaySources,connectionDate,secureProfileImageUrl&sort=CREATED_DESC&source=LINKEDIN&_=1481543279665"
connections_url = "https://www.linkedin.com/profile/profile-v2-connections?id=396532726&offset=10&count=20&distance=1&type=SHARED"

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
        f.write(json.dumps(self.loadPage(contacts_url)))


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

parser = LinkedInParser(username, passphrase)