import json
import extractor_api.settings as settings
from . import controllers, utils
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from api.models import Job
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LinkedInView(APIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LinkedInView, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data['graph_name']
            username = data['username']
            password = data['password']
            user_id = int(data['user_id'])
        except Exception:
            payload = utils.ResponsePayload()
            payload.message = 'Valid LinkedIn username, password and name required.'
            return JsonResponse(payload.__dict__, status=status.HTTP_400_BAD_REQUEST)

        payload = controllers.process_linkedin_run(name, username, password, user_id)

        return JsonResponse(payload.__dict__, status=status.HTTP_200_OK)


class TwitterView(APIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TwitterView, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data['graph_name']
            screen_name = data['screen_name']
            user_id = int(data['user_id'])
        except Exception:
            payload = utils.ResponsePayload()
            payload.message = 'Something went wrong. Please try again'
            return JsonResponse(payload.__dict__, status=status.HTTP_400_BAD_REQUEST)

        payload = controllers.process_twitter_run(name, user_id, screen_name)

        return JsonResponse(payload.__dict__, status=status.HTTP_200_OK)


class JobsView(ViewSet):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    """
    Get Job by id
    """
    def get_by_id(self, request, pk, format=None):

        try:
            payload = controllers.process_get_job_by_id(pk)
        except Job.DoesNotExist:
            payload_failed = utils.ResponsePayload(message='Job with id: %s not found' % pk)
            return JsonResponse(data=payload_failed.__dict__, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse(data=payload.__dict__, status=status.HTTP_200_OK)

    """
    Get Jobs by user id
    """
    def get_by_user_id(self, request, user_id, format=None):
        # Default is -1 which returns all
        count = request.GET.get('count', -1)
        page = int(request.GET.get('page', 0))

        try:
            if not type(count) == int:
                count = int(count)
        except ValueError:
            count = 0

        if page > 0:
            payload = controllers.paginate_jobs_by_user_id(user_id, page)
        else:
            payload = controllers.process_get_job_by_user_id(user_id, count)

        return JsonResponse(data=payload.__dict__, status=status.HTTP_200_OK)

    """
    Get Job Summary
    """
    def get_summary(self, request, user_id, format=None):

        payload = controllers.process_get_user_job_summary(user_id)

        return JsonResponse(data=payload.__dict__, status=status.HTTP_200_OK)

    def publish_endpoints(self, request, format=None):
        return JsonResponse(data=settings.ENDPOINTS, status=status.HTTP_200_OK)
