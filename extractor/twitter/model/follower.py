# This is the model for a Twitter follower
class Follower(object):

    def __init__(self, user_id, handle, name, description, is_following, is_default_picture):
        self._user_id = user_id
        self._handle = handle
        self._name = name
        self._description = description
        self._is_following = is_following
        self._is_default_picture = is_default_picture

    @property
    def id(self):
        return self._user_id

    @id.setter
    def handle(self, user_id):
        self._user_id = user_id

    @property
    def handle(self):
        return self._handle

    @handle.setter
    def handle(self, handle):
        self._handle = handle

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def is_following(self):
        return self._is_following

    @is_following.setter
    def is_following(self, is_following):
        self._is_following = is_following

    @property
    def is_default_picture(self):
        return self._is_default_picture

    @is_default_picture.setter
    def is_default_picture(self, is_default_picture):
        self._is_default_picture = is_default_picture
