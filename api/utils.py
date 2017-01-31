import time
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    try:
        detail = response.data['detail']
    except AttributeError:
        detail = exc

    res = ResponsePayload(detail)

    return JsonResponse(res.__dict__, status=exc.status_code)


def server_error(request):
    res = ResponsePayload('Server Error')
    return JsonResponse(res.__dict__, status.HTTP_500_INTERNAL_SERVER_ERROR)


def not_found(request):
    res = ResponsePayload('Not Found')
    return JsonResponse(res.__dict__, status=status.HTTP_404_NOT_FOUND)


def permission_denied(request):
    res = ResponsePayload('Access Denied')
    return JsonResponse(res.__dict__, status=status.HTTP_403_FORBIDDEN)


def bad_request(request):
    res = ResponsePayload('Bad Request')
    return JsonResponse(res.__dict__, status=status.HTTP_400_BAD_REQUEST)


def generate_timestamp():
    return int(round(time.time() * 1000))


class ResponsePayload(object):

    def __init__(self, message):
        self.message = message
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)



