import jsonpickle

from django.http import HttpResponse
from extractor import LinkedInParser


def index(request):
    network = LinkedInParser().mockNetwork()
    return HttpResponse(jsonpickle.encode(network, unpicklable=False))
