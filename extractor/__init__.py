"""
Extractor entry point which is called by
the api entry point. The service is run on
a thread.
"""
import api.utils as utils
import extractor_api.settings as config
from extractor.persistence.bulk_loader import BulkLoader, BulkLoaderException
from api.models import Job
from extractor.persistence.connector import Driver
from extractor.model.network import Network
from extractor.image_generator import ImageGenerator
from extractor.crawlers.twitter import get_friends, twitter_network

is_prod = config.ENV == 'PROD'


def run_linkedin(job, username, password):
    import extractor.crawlers.linkedin.linkedin as linkedin
    msg = ''
    failed = False

    if is_prod:
        graph, root_id = linkedin.LinkedInCrawler(username, password).launch()
        if isinstance(graph, Exception):
            msg = str(graph)
            failed = True
        else:
            loader = BulkLoader()
            image_gen = ImageGenerator(graph)
            driver = Driver()
            network = Network(job.name, job.id, utils.generate_timestamp(),
                              len(graph.nodes()), job.type.description, image_gen.get_image_ref())
            try:
                query = loader.get_query(graph, 'Connection', 'CONNECTED_TO')
                driver.link_graph_to_user(job.user_id, root_id, network.__dict__, query)
            except BulkLoaderException as e:
                msg = str(e)
                failed = True

    on_complete(job, failed, msg)


def run_twitter(job, screen_name):
    msg = ''
    failed = False

    if is_prod:

        try:
            seed_id = get_friends.run(screen_name)
            graph = twitter_network.generate_graph(seed_id=seed_id)
            print('done')
        except Exception as error:
            msg = str(error)
            failed = True

    on_complete(job, failed, msg)


def on_complete(job, failed, msg):
    if not failed and is_prod:
        msg = 'Successfully imported'
    elif not is_prod:
        msg = 'Extractor did not run, environment not production'
        failed = True

    Job.update(job_id=job.id, status=msg, is_complete=True,
               is_success=not failed, end_time=utils.generate_timestamp())
