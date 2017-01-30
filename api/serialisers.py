from rest_framework import serializers
from api.models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'user_id', 'status', 'type', 'start_time', 'end_time')
