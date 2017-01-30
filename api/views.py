import json
import api.controllers as controller
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Job
from api.utils import ResponseTemplate


@csrf_exempt
@api_view(['POST'])
def linkedin_run(request):

    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
        user_id = int(data['user_id'])
    except Exception:
        res = ResponseTemplate('')
        res.message = 'Valid LinkedIn username and password, and exograph user_id is required'
        return JsonResponse(res.__dict__, status=status.HTTP_400_BAD_REQUEST)

    res = controller.process_linkedin_run(username, password, user_id)

    return JsonResponse(res.__dict__, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_job_by_id(request, pk):

    try:
        res = controller.process_get_job_by_id(pk)
    except Job.DoesNotExist:
        res_failed = ResponseTemplate('Job with id: %s not found' % pk)
        return JsonResponse(data=res_failed.__dict__, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse(data=res.__dict__, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_jobs_by_user_id(request, user_id):

    res = controller.process_get_job_by_user_id(user_id)

    return JsonResponse(data=res.__dict__, status=status.HTTP_200_OK)
