from rest_framework import serializers
from api.models import Job, JobType


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'user_id', 'status', 'type', 'complete', 'start_time', 'end_time')


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ('description',)


