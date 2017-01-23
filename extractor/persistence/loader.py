import config as conf
import extractor.linkedin.LinkedInParser as parser
from neo4jrestclient.client import GraphDatabase

config = conf.Config().neo4j()
network = parser.LinkedInParser().mockNetwork()
db = GraphDatabase(config['host'], config['username'], config['password'])

del network[0]

connection = db.labels.create("Connection")
for node in network:

    c = db.nodes.create(name=node.name, title=node.title, company=node.company, distance=node.distance,
                        profileImage=node.profileImageUrl, profile=node.profileUrl)
    connection.add(c)
