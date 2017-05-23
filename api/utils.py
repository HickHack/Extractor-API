import time
from threading import Timer
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

    if exc.status_code:
        status = exc.status_code
    else:
        status = 500

    return JsonResponse(res.__dict__, status=status)


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
    return round(time.time())


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class ResponsePayload(object):
    def __init__(self, message='', summary=None):
        self.message = message
        self.jobs = []
        self.count = 0
        self.pagination = {}
        if isinstance(summary, JobsSummary):
            self.summary = summary.__dict__
        else:
            self.summary = summary

    def add_job(self, job):
        self.jobs.append(job)
        self.count += 1


class JobsSummary(object):
    def __init__(self, user_id, warning_count, running_count):
        self.user_id = user_id
        self.warning_count = warning_count
        self.running_count = running_count
