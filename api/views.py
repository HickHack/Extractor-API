import json
import api.controllers as controller
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from api.models import Job
from api.utils import ResponsePayload
from api.auth import CsrfExemptSessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class ExtractorAPI(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, JSONWebTokenAuthentication)

    def post(self, request):

        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data['username']
            password = data['password']
            user_id = int(data['user_id'])
        except Exception:
            payload = ResponsePayload('')
            payload.message = 'Valid LinkedIn username and password, and exograph user_id is required'
            return JsonResponse(payload.__dict__, status=status.HTTP_400_BAD_REQUEST)

        payload = controller.process_linkedin_run(username, password, user_id)

        return JsonResponse(payload.__dict__, status=status.HTTP_200_OK)


class JobsAPI(ViewSet):

    authentication_classes = (CsrfExemptSessionAuthentication, JSONWebTokenAuthentication)

    def __init__(self, **kwargs):
        super(JobsAPI, self).__init__(**kwargs)

    """
    Get Job by id
    """
    def get_by_id(self, request, pk, format=None):

        try:
            payload = controller.process_get_job_by_id(pk)
        except Job.DoesNotExist:
            payload_failed = ResponsePayload('Job with id: %s not found' % pk)
            return JsonResponse(data=payload_failed.__dict__, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse(data=payload.__dict__, status=status.HTTP_200_OK)

    """
    Get Jobs by user id
    """
    def get_by_user_id(self, request, user_id, format=None):

        payload = controller.process_get_job_by_user_id(user_id)

        return JsonResponse(data=payload.__dict__, status=status.HTTP_200_OK)
