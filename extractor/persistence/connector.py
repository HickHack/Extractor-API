from extractor_api.settings import NEO4J
from neo4j.v1 import GraphDatabase, basic_auth


class Driver(object):
    def __init__(self):
        self.host = ''
        self.username = ''
        self.password = ''

        self.parse_settings()
        self.driver = GraphDatabase.driver(self.host, auth=basic_auth(self.username, self.password))

    def parse_settings(self):
        try:
            default = NEO4J['default']

            self.host = 'bolt://%s:%s' % (default['HOST'], default['PORT'])
            self.username = default['USERNAME']
            self.password = default['PASSWORD']
        except KeyError:
            raise DriverParseException('Unable to load database settings')

    # This is a bit hacky because py2neo doesn't yet support
    # queries of this level using their Object Graph Mapper (OGM)
    # TODO: Run queries in one transaction
    def link_graph_to_user(self, user_id, root_id, attr_dict, social_graph_query):
        session = self.driver.session()

        session.run(social_graph_query)

        session.run('CREATE (a:SubGraph {name: {name}, job_id: {job_id},'
                    'created_time: {created_time}, no_connections: {no_connections},'
                    'type: {type}})',
                    attr_dict)

        session.run('MATCH (u:User) WHERE id(u)= {user_id}'
                    'OPTIONAL MATCH (g:SubGraph {job_id: {job_id}}) '
                    'OPTIONAL MATCH (c:Connection {member_id: {root_id}}) '
                    'CREATE (u)-[:OWNS]->(g)-[:CONTAINS]->(c)',
                    {'user_id': user_id, 'job_id': attr_dict['job_id'], 'root_id': root_id})

        session.close()


class DriverParseException(Exception):
    def __init__(self, message):
        super(DriverParseException, self).__init__(message)

