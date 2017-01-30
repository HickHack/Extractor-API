"""
Controllers that are used by the API views
by using MVC it makes the controllers more
testable instead of having controller and model
logic residing in the views
"""

import extractor
import api.utils as utils
from threading import Thread
from api.models import JobType, Job
from api.utils import ResponseTemplate
from api.serialisers import JobSerializer


def process_linkedin_run(username, password, user_id):
    res = ResponseTemplate('')

    thread = Thread(target=extractor.run_linkedin, args=(username, password))
    thread.start()

    job = Job(user_id=user_id, status='running',
              type=JobType.objects.get(pk=1), start_time=utils.generate_timestamp())
    job.save()

    serialised = JobSerializer(job)
    res.add_job(serialised.data)

    return res


def process_get_job_by_id(pk):
    res = ResponseTemplate('')

    job = Job.objects.get(pk=pk)
    serialized = JobSerializer(job)
    res.add_job(serialized.data)

    return res


def process_get_job_by_user_id(user_id):
    res = ResponseTemplate('')

    jobs_set = Job.objects.all().filter(user_id=user_id)

    for job in jobs_set.iterator():
        serialized = JobSerializer(job)
        data = serialized.data
        data['type'] = job.type.description
        res.add_job(data)

    return res
