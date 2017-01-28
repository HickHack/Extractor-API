"""
Extractor entry point which is called by
the api entry point. The service is run on
a thread
"""

import time
from extractor.crawlers.linkedin import LinkedInCrawler
from extractor.persistence.bulk_loader import BulkLoader


def run_linkedin(username, password):
    start_time = int(round(time.time()))

    graph = LinkedInCrawler.mock_network()
    loader = BulkLoader()
    status = loader.load(graph, 'Connection', 'CONNECTED_TO')

    end_time = int(round(time.time()))

    print("Total Time Taken: %d seconds" % (end_time - start_time))