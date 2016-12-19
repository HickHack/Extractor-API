# This is the model for a LinkedIn connection


class Connection(object):

    def __init__(self, member_id, name, title, company, distance, profileImageUrl, profileUrl):
        self._member_id = member_id
        self._name = name
        self._title = title
        self._company = company
        self._distance = distance
        self._profileImageUrl = profileImageUrl
        self._profileUrl = profileUrl
        self._sharedConnections = []

    @staticmethod
    def fromDict(connection):
        return Connection(connection['_member_id'], connection['_name'], connection['_title'],
                          connection['_company'], connection['_distance'], connection['_profileImageUrl'],
                          connection['_profileUrl'])

    @property
    def member_id(self):
        return self._member_id

    @member_id.setter
    def member_id(self, member_id):
        self._member_id = member_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, company):
        self._company = company

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, distance):
        if distance.contains('_'):
            split = distance.split('_')
            self._distance = int(split[1])
        else:
            self._distance = distance

    @property
    def profileImageUrl(self):
        return self._profileImageUrl

    @profileImageUrl.setter
    def profileImageUrl(self, profileImgUrl):
        self._profileImageUrl = profileImgUrl

    @property
    def profileUrl(self):
        return self._profileUrl

    @profileUrl.setter
    def profileUrl(self, profileUrl):
        self._profileUrl = profileUrl

    @property
    def sharedConnections(self):
        return self._sharedConnections

    @sharedConnections.setter
    def sharedConnections(self, sharedConnection):
        self._sharedConnections = sharedConnection

    def addConnection(self, connection):
        self._sharedConnections.append(connection)



