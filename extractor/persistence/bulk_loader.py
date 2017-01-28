"""
Convert NetworkX graph to a neo4j cypher query
This is based on an improved version
of an example on GitHub by aanastasiou

Anastasiou, A. (2012) Generate a Cypher query to store a python NetworkX directed graph.
Available at: https://gist.github.com/aanastasiou/6099561
(Accessed: 27 January 2017).
"""

import random
from neo4j.v1 import GraphDatabase, basic_auth

letter_dct = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
num_dct = "0123456789"


class BulkLoader(object):
    def __init__(self):

        self._node_statements = {}
        self._edge_statements = []
        self._graph = None
        self._label = None
        self._rel = None
        self._status = {'success': False, 'mgs': ''}

    def load(self, graph, label, rel='KNOWS', host='bolt://localhost:7687'):
        self._graph = graph
        self._label = label
        self._rel = rel

        cypher = self.generate_cypher()

        try:
            driver = GraphDatabase.driver(host, auth=basic_auth("neo4j", ""))
            session = driver.session()

            session.run(cypher)

            session.close()

            self._status['success'] = True

        except Exception as e:
            self._status['success'] = False
            self._status['msg'] = e.message

        finally:
            return self._status

    def generate_cypher(self):
        self.generate_node_statements()
        self.generate_edge_statements()

        # Put both definitions together and return the create statement.
        return "CREATE %s,%s;\n" % (
            ",".join(map(lambda x: x[1][1], self._node_statements.items())), ",".join(self._edge_statements))

    def generate_node_statements(self):
        # Partially generate the node representations
        for node in self._graph.nodes(data=True):
            # Generate a node identifier for Cypher
            identifier = self.generate_tag(5) + self.generate_tag(6, dct=num_dct)

            # Append the node's ID attribute so that the node-ID information used by Networkx is preserved.
            node_items = node[1].items()

            # Create the key-value representation of the node's attributes taking care to add quotes when the value is of type string
            node_attributes = "{%s}" % ",".join(
                map(lambda x: "%s:%s" % (x[0], x[1]) if not type(x[1]) == str else "%s:'%s'" % (x[0], x[1]),
                    node_items))

            # Store it to a dictionary indexed by the node-id.
            self._node_statements[node[0]] = [identifier, "(%s:%s %s)" % (identifier, self._label, node_attributes)]

    @staticmethod
    def generate_tag(length, dct=letter_dct):
        return ''.join([dct[random.randint(0, len(dct) - 1)] for i in range(0, length)])

    def generate_edge_statements(self):
        # Generate the relationship representations
        for edge in self._graph.edges(data=True):
            edge_items = edge[2].items()

            edge_attributes = ""
            if len(edge_items) > 0:
                edge_attributes = "{%s}" % ",".join(
                    map(lambda x: "%s:%s" % (x[0], x[1]) if not type(x[1]) == str else '%s:"%s"' % (x[0], x[1]),
                        edge_items))

            # NOTE: Declare the links by their Cypher node-identifier rather than their Networkx node identifier
            self._edge_statements.append("(%s)-[:%s %s]->(%s)" % (
                self._node_statements[edge[0]][0], self._rel, edge_attributes, self._node_statements[edge[1]][0]))
