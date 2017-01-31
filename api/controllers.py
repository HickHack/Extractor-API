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
from api.utils import ResponsePayload
from api.serialisers import JobSerializer


def process_linkedin_run(username, password, user_id):
    payload = ResponsePayload('')

    thread = Thread(target=extractor.run_linkedin, args=(username, password))
    thread.start()

    job = Job(user_id=user_id, status='running',
              type=JobType.objects.get(description="LINKEDIN"), start_time=utils.generate_timestamp())
    job.save()

    data = form_job(job)
    payload.add_job(data)

    return payload


def process_get_job_by_id(pk):
    payload = ResponsePayload('')

    job = Job.objects.get(pk=pk)
    data = form_job(job)
    payload.add_job(data)

    return payload


def process_get_job_by_user_id(user_id):
    payload = ResponsePayload('')

    jobs_set = Job.objects.all().filter(user_id=user_id)

    for job in jobs_set.iterator():
        data = form_job(job)
        payload.add_job(data)

    return payload


def form_job(job):
    serialized = JobSerializer(job)
    data = serialized.data
    data['type'] = job.type.description

    return data
