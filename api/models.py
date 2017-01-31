from django.db import models
from rest_framework.authtoken.models import Token


class JobType(models.Model):
    description = models.CharField(max_length=100)


class Job(models.Model):
    user_id = models.IntegerField()
    status = models.CharField(max_length=100)
    complete = models.BooleanField(default=False)
    type = models.ForeignKey(JobType)
    start_time = models.BigIntegerField(default=0)
    end_time = models.BigIntegerField(default=0)

