"""
LinkedIn Connection model
"""

import base64
from random import randint


class Connection(object):

    def __init__(self, member_id, name,
                 title, company, email,
                 phone, location, connection_date,
                 member_since, profile_image_url, profile_url,
                 is_root=False):

        self.member_id = member_id
        self.name = self.clean(name)
        self.title = self.clean(title)
        self.company = self.clean(company)
        self.email = self.clean(email)
        self.phone = self.clean(phone)
        self.location = self.clean(location)
        self.connection_date = connection_date
        self.member_since = member_since
        self.profile_image_url = base64.b64encode(profile_image_url.encode('utf-8')).decode('utf-8')
        self.profile_url = base64.b64encode(profile_url.encode('utf-8')).decode('utf-8')
        self.is_root = is_root
        self.connections = []

    def addConnection(self, node):
        self.connections.append(node)

    @staticmethod
    def parse_contact(connection):
        member_id = connection['memberId'] if connection.get('memberId') else randint(0, 8000)
        name = connection['fullName'] if connection.get('fullName') else ''
        title = connection['title'] if connection.get('title') else ''
        company = connection['company']['name'] if connection.get('company') else ''
        profile_image_url = connection['profileImageUrl'] if connection.get('profileImageUrl') else ''
        profile_url = connection['profileUrl'] if connection.get('profileUrl') else ''
        email = connection['emails'][0]['emailAddress'] if len(connection['emails']) != 0 else ''
        phone = connection['phoneNumbers'][0]['number'] if len(connection['phoneNumbers']) != 0 else ''
        location = connection['location'] if connection.get('location') else ''
        connection_date = connection['connectionDate'] if connection.get('connectionDate') else 0
        member_since = connection['created'] if connection.get('created') else 0

        return Connection(member_id, name, title,
                          company, email, phone,
                          location, connection_date, member_since,
                          profile_image_url, profile_url)

    @staticmethod
    def parse_shared_connection(connection):
        member_id = connection['memberID'] if connection.get('memberID') else 0
        name = connection['fmt__full_name'] if connection.get('fmt__full_name') else ''
        title = connection['headline'] if connection.get('headline') else ''
        profile_image_url = connection['mem_pic'] if connection.get('mem_pic') else ''
        profile_url = connection['pview'] if connection.get('pview') else ''

        return Connection(member_id, name, title,
                          '', '', '',
                          '', '', '',
                          profile_image_url, profile_url)

    @staticmethod
    def clean(val):
        return val.replace("'", '')
