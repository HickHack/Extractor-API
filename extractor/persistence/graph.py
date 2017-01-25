from neo4jrestclient.client import GraphDatabase

from extractor.linkedin.model.connection import Connection
from extractor.linkedin.LinkedInParser import Graph

# Root
g = Connection('G', 'Graham', 'Engineer', 'Workday', 0, 'graham.png', 'graham.com')

j = Connection('J', 'John', '', '', 1, '', '')
c = Connection('C', 'Craig', '', '', 1, '', '')
s = Connection('S', 'Sam', '', '', 1, '', '')

e = Connection('E', 'Eamon', '', '', 1, '', '')
c = Connection('C', 'Crag', '', '', 1, '', '')

s = Connection('S', 'Sam', '', '', 1, '', '')
e = Connection('E', 'Eamon', '', '', 1, '', '')

c = Connection('C', 'Craig', '', '', 1, '', '')


G = Graph()

# Add Root Node
G.add_node(g.member_id, g.__dict__)

# Add all the direct contacts
G.add_node(j.member_id, j.__dict__)
G.add_edge(g.member_id, j.member_id)

G.add_node(e.member_id, e.__dict__)
G.add_edge(g.member_id, e.member_id)

G.add_node(c.member_id, c.__dict__)
G.add_edge(g.member_id, c.member_id)

G.add_node(s.member_id, s.__dict__)
G.add_edge(g.member_id, s.member_id)

# Start the process of looking at shared connections, start at root[i = 0] = John
# j -> c
G.add_edge(j.member_id, c.member_id)

# j -> s
G.add_edge(j.member_id, s.member_id)

# root[i = 1] = Eamon
# e -> c
G.add_edge(e.member_id, c.member_id)

# root[i = 2] = Sam
G.add_edge(s.member_id, e.member_id)

# root[i = 3] = Craig

G.draw()
G.write_to_file()


