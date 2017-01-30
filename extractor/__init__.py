"""
Extractor entry point which is called by
the api entry point. The service is run on
a thread
"""

import extractor.crawlers.linkedin as linkedin
from extractor.persistence.bulk_loader import BulkLoader
from extractor.config import Config

config = Config()


def run_linkedin(username, password):
    if config.env()['env'] != 'TEST':
        graph = linkedin.LinkedInCrawler(username, password).launch()

        if isinstance(graph, Exception):
            # TODO log exception
            print('Crawler Failed')
        else:
            loader = BulkLoader()
            status = loader.load(graph, 'Connection', 'CONNECTED_TO')

            if not status['success']:
                print('Bulk Load Failure')
