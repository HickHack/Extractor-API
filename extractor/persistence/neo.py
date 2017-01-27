"""
Convert NetworkX graph to a neo4j cypher query
This is based on a refactored and mutated version

Anastasiou, A. (2012) Generate a Cypher query to store a python NetworkX directed graph.
Available at: https://gist.github.com/aanastasiou/6099561
(Accessed: 27 January 2017).

"""
import random

# Simple character lists
letter_dct = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
num_dct = "0123456789"

node_statements = {}
edge_statements = []


def generate_tag(length, dct=letter_dct):
    return ''.join([dct[random.randint(0, len(dct) - 1)] for i in range(0, length)])


def graph_2_cypher(G, label, rel='KNOWS'):

    generate_node_statements(G, label)
    generate_edge_statements(G, rel)

    # Put both definitions together and return the create statement.
    return "CREATE %s,%s;\n" % (",".join(map(lambda x: x[1][1], node_statements.items())), ",".join(edge_statements))


def generate_node_statements(G, label):
    # Partially generate the node representations
    for node in G.nodes(data=True):
        # Generate a node identifier for Cypher
        identifier = generate_tag(5) + generate_tag(6, dct=num_dct)

        # Append the node's ID attribute so that the node-ID information used by Networkx is preserved.
        node_items = node[1].items()

        # Create the key-value representation of the node's attributes taking care to add quotes when the value is of type string
        node_attributes = "{%s}" % ",".join(
            map(lambda x: "%s:%s" % (x[0], x[1]) if not type(x[1]) == str else "%s:'%s'" % (x[0], x[1]), node_items))

        # Store it to a dictionary indexed by the node-id.
        node_statements[node[0]] = [identifier, "(%s:%s %s)" % (identifier, label, node_attributes)]


def generate_edge_statements(G, rel):
    # Generate the relationship representations
    for edge in G.edges(data=True):
        edge_items = edge[2].items()

        edge_attributes = ""
        if len(edge_items) > 0:
            edge_attributes = "{%s}" % ",".join(
                map(lambda x: "%s:%s" % (x[0], x[1]) if not type(x[1]) == str else '%s:"%s"' % (x[0], x[1]),
                    edge_items))

        # NOTE: Declare the links by their Cypher node-identifier rather than their Networkx node identifier
        edge_statements.append("(%s)-[:%s %s]->(%s)" % (
            node_statements[edge[0]][0], rel, edge_attributes, node_statements[edge[1]][0]))
