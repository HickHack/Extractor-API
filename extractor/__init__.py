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

is_prod = settings.ENV == 'PROD'


def run_linkedin(job_id, username, password):
    import extractor.crawlers.linkedin as linkedin

    failed = False

    if is_prod:
        result = linkedin.LinkedInCrawler(username, password).launch()
        if isinstance(result, Exception):
            msg = str(result)
            failed = True
        else:
            loader = BulkLoader()

            try:
                loader.load(result, 'Connection', 'CONNECTED_TO')
            except BulkLoaderException as e:
                msg = str(e)
                failed = True

    if not failed and is_prod:
        msg = 'Successfully imported'
    elif not is_prod:
        msg = 'Extractor did not run, environment not production'
        failed = True

    Job.update(job_id=job_id, status=msg, is_complete=True,
               is_success=not failed, end_time=utils.generate_timestamp())





