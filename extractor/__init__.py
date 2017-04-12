"""
Extractor entry point which is called by
the api entry point. The service is run on
a thread.
"""
import api.utils as utils
import extractor_api.settings as config
import extractor.persistence as persistence
from api.models import Job
from extractor.model.network import Network
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

            try:
                persistence.load(graph, root_id, job, label='Connection', rel='CONNECTED_TO')
            except Exception as e:
                msg = str(e)
                failed = True

    on_complete(job, failed, msg)


def run_twitter(job, screen_name):
    msg = ''
    failed = False

    if is_prod:

        try:
            root_id = get_friends.run(screen_name)
            graph, root_uuid = twitter_network.generate_graph(seed_id=root_id)
            persistence.load(graph, root_uuid, job, label='Follower', rel='IS_FOLLOWING')
        except Exception as error:
            msg = 'Failed to fetch graph'
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

