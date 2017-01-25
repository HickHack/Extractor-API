# This is the model for a LinkedIn connection


class Connection(object):

    def __init__(self, member_id, name, title, company, distance, profileImageUrl, profileUrl):
        self.member_id = member_id
        self.name = name
        self.title = title
        self.company = company
        self.distance = distance
        self.profileImageUrl = profileImageUrl
        self.profileUrl = profileUrl
        self.connections = []

    def addConnection(self, node):
        self.connections.append(node)