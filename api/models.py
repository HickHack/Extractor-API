import time
from django.db import models


class ResponseTemplate(object):

    def __init__(self, message, jobs=[]):
        self.message = message
        self.jobs = jobs


class JobType(models.Model):
    description = models.CharField(max_length=100)


class Job(models.Model):
    user_id = models.IntegerField()
    status = models.CharField(max_length=100)
    type = models.ForeignKey(JobType)
    start_time = models.BigIntegerField(default=int(round(time.time() * 1000)))
    end_time = models.BigIntegerField(default=0)

