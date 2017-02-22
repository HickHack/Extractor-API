"""
Extractor entry point which is called by
the api entry point. The service is run on
a thread.
"""
import api.utils as utils
from extractor.persistence.bulk_loader import BulkLoader, BulkLoaderException
from extractor.config import Config
from api.models import Job
from extractor_api import settings
from extractor.persistence.connector import Driver
from extractor.model.network import Network
from extractor.image_generator import ImageGenerator

is_prod = settings.ENV == 'PROD'


def run_linkedin(job, username, password):
    import extractor.crawlers.linkedin as linkedin

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

    if not failed and is_prod:
        msg = 'Successfully imported'
    elif not is_prod:
        msg = 'Extractor did not run, environment not production'
        failed = True

    Job.update(job_id=job.id, status=msg, is_complete=True,
               is_success=not failed, end_time=utils.generate_timestamp())
