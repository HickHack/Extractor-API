"""
Model representing a Twitter User
"""

import re
import os
import json
import base64
import uuid
import extractor.settings as settings


class User(object):
    def __init__(self, name, screen_name, id,
                 friends_count, followers_count, location,
                 profile_image_url, member_since, description,
                 friends_ids=None, followers_ids=None, u_uuid=None):

        if followers_ids is None:
            followers_ids = []

        if friends_ids is None:
            friends_ids = []

        self.name = name
        self.screen_name = screen_name
        self.id = id
        self.friends_count = friends_count
        self.followers_ids = followers_ids
        self.friends_ids = friends_ids
        self.followers_count = followers_count
        self.location = self.encode_data(location)
        self.member_since = member_since
        self.profile_image_url = self.encode_data(self.clean_image_profile_url(profile_image_url))
        self.profile_url = self.encode_data(self.create_profile_url(screen_name))
        self.description = self.encode_data(self.clean_description(description))
        self.uuid = u_uuid
        self.generate_uuid()
        self.clean()

    @staticmethod
    def clean_image_profile_url(url):
        return url.replace('_normal', '')

    @staticmethod
    def clean_description(description):
        return re.sub(r'\\', r'', description)

    @staticmethod
    def create_profile_url(screen_name):
        return "https://twitter.com/" + screen_name

    @staticmethod
    def create(user_dict, skip_followers_ids=True):
        user = user_dict

        if skip_followers_ids:
            followers_ids = []
        else:
            followers_ids = user.followers_ids()

        return User(name=user.name, screen_name=user.screen_name,
                    id=user.id, friends_count=user.friends_count,
                    followers_count=user.followers_count, location=user.location,
                    member_since=int(user.created_at.timestamp()), description=user.description,
                    profile_image_url=user.profile_image_url, followers_ids=followers_ids)

    @staticmethod
    def load(id):
        user_path = User.get_path(id)

        if User.exists(id):
            with open(user_path, "r") as f:
                user = json.loads(f.read())
            return User(name=user['name'], screen_name=user['screen_name'],
                        id=user['id'], friends_count=user['friends_count'],
                        followers_count=user['followers_count'], location=user['location'],
                        member_since=user['member_since'], description=user['description'],
                        profile_image_url=user['profile_image_url'], friends_ids=user['friends_ids'],
                        followers_ids=user['followers_ids'], u_uuid=user['uuid'])
        return None

    @staticmethod
    def encode_data(data):
        match = re.match('^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)+$', data)

        if not match:
            return base64.b64encode(data.encode('utf-8')).decode('utf-8')
        elif data == '':
            return ''

        return data

    @staticmethod
    def exists(id):
        return os.path.exists(User.get_path(id))

    @staticmethod
    def get_path(id):
        return os.path.join(settings.TWITTER['cache']['users'], str(id) + '.json')

    def persist(self):
        with open(self.get_path(self.id), 'w') as out_file:
            out_file.write(json.dumps(self.__dict__))

    def has_discovered_friends(self):
        return settings.TWITTER['limits']['max_friends'] >= len(self.friends_ids) > 0

    def add_friend(self, id):
        self.friends_ids.append(id)

    def set_followers_ids(self, followers_ids):
        self.followers_ids = followers_ids

    def get_attributes(self):
        return {
            'name': self.name,
            'screen_name': self.screen_name,
            'id': self.id,
            'friends_count': self.friends_count,
            'followers_count': self.followers_count,
            'location': self.location,
            'member_since': self.member_since,
            'description': self.description,
            'profile_image_url': self.profile_image_url,
            'profile_url': self.profile_url,
            'uuid': self.uuid
        }

    def clean(self):
        self.name = self.name.replace("'", '')
        self.name = self.name.replace(",", '')

    def generate_uuid(self):
        if self.uuid is None:
            self.uuid = str(uuid.uuid4())

    def regenerate_uuid(self):
        """ Reset UUID. If it is the same generate another one """
        new_uuid = str(uuid.uuid4())

        if not new_uuid == self.uuid:
            self.uuid = new_uuid
        else:
            self.uuid = str(uuid.uuid4())
