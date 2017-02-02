from django.db import models
from rest_framework.authtoken.models import Token


class JobType(models.Model):
    description = models.CharField(max_length=100)


class Job(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=300, default='')
    status = models.CharField(max_length=100)
    complete = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    type = models.ForeignKey(JobType)
    start_time = models.BigIntegerField(default=0)
    end_time = models.BigIntegerField(default=0)
    total_time = models.BigIntegerField(default=0)

    @staticmethod
    def update(job_id, status, is_complete, is_success, end_time):
        job = Job.objects.get(id=job_id)

        job.status = status
        job.complete = is_complete
        job.success = is_success
        job.end_time = end_time
        job.total_time = end_time - job.start_time

        job.save()









