# This is the model for a LinkedIn connection


class Connection(object):

    def __init__(self, member_id, name, title, company, headline, distance, profileImageUrl, profileUrl):
        self._member_id = member_id
        self._name = name
        self._title = title
        self._company = company
        self._headline = headline
        self._distance = distance
        self._profileImageUrl = profileImageUrl
        self._profileUrl = profileUrl

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
    def headline(self):
        return self._headline

    @headline.setter
    def headline(self, headline):
        self._headline = headline

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, distance):
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



