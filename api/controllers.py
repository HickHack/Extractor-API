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
from api.utils import ResponsePayload, JobsSummary
from api.serialisers import JobSerializer


def process_linkedin_run(name, username, password, user_id):
    payload = ResponsePayload()

    job = Job(user_id=user_id, status='running',
              type=JobType.objects.get(description="LINKEDIN"), start_time=utils.generate_timestamp(),
              name=name)
    job.save()

    thread = Thread(target=extractor.run_linkedin, args=(job, username, password))
    thread.start()

    data = form_job(job)
    payload.add_job(data)

    return payload


def process_twitter_run(name, user_id, screen_name):
    payload = ResponsePayload()

    job = Job(user_id=user_id, status='running',
              type=JobType.objects.get(description="TWITTER"), start_time=utils.generate_timestamp(),
              name=name)
    job.save()

    thread = Thread(target=extractor.run_twitter, args=(job, screen_name))
    thread.start()

    data = form_job(job)
    payload.add_job(data)

    return payload


def process_get_job_by_id(pk):
    payload = ResponsePayload()

    job = Job.objects.get(pk=pk)
    data = form_job(job)
    payload.add_job(data)

    return payload


def process_get_job_by_user_id(user_id, count=-1):
    payload = ResponsePayload()

    if count == -1:
        jobs_set = Job.objects.all().filter(user_id=user_id)
    else:
        if count > 0:
            jobs_set = Job.objects.all().filter(user_id=user_id).order_by('-id')[:count]

    for job in jobs_set.iterator():
        data = form_job(job)
        payload.add_job(data)

    return payload


def form_job(job):
    serialized = JobSerializer(job)
    data = serialized.data
    data['type'] = job.type.description

    return data


def process_get_user_job_summary(user_id):
    running_count = Job.objects.all().filter(user_id=user_id, complete=False).count()

    summary = JobsSummary(user_id=user_id, warning_count=3, running_count=running_count)
    payload = ResponsePayload(summary=summary)

    return payload

