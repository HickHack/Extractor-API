import extractor.persistence.neo as graph2Cypher

from neo4j.v1 import GraphDatabase, basic_auth
from extractor.crawlers.linkedin import LinkedInCrawler

G = LinkedInCrawler.mock_network()
query = graph2Cypher.graph_2_cypher(G, 'Connection', 'CONNECTED_TO')

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", ""))
session = driver.session()

print(query)

r = session.run(query)
session.close()
