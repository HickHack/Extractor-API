import extractor
import json
from threading import Thread
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from api.models import ResponseTemplate, Job, JobType
from api.serialisers import JobSerializer


@csrf_exempt
@api_view(['POST'])
def linkedin_run(request):
    res = ResponseTemplate('')

    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
    except Exception as e:
        res.message = 'Valid LinkedIn username and password is required'
        return JsonResponse(res.__dict__, status=status.HTTP_400_BAD_REQUEST)

    thread = Thread(target=extractor.run_linkedin, args=(username, password))
    thread.start()

    job = Job(user_id=12, status='running', type=JobType.objects.get(pk=1))
    job.save()

    serialised = JobSerializer(job)
    res.jobs = [serialised.data]

    return JsonResponse(res.__dict__, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_job_by_id(request, pk):
    res = ResponseTemplate('')

    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        res.message = 'Item with id: %s not found' % pk
        return JsonResponse(res.__dict__, status=status.HTTP_404_NOT_FOUND)

    serialized = JobSerializer(job)
    res.jobs = [serialized.data]

    return JsonResponse(data=res.__dict__, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['GET'])
def get_jobs_by_user_id(request, user_id):
    return JsonResponse({}, status=status.HTTP_200_OK)
