import extractor
from django.http import HttpResponse
from threading import Thread


def index(request):
    username = ''
    password = ''

    thread = Thread(target=extractor.run_linkedin, args=(username, password))
    thread.start()

    return HttpResponse('Job Running eta 5 mins')
