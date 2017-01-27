import jsonpickle

from django.http import HttpResponse
from extractor import LinkedInCrawler


def index(request):
    network = LinkedInCrawler().mock_network()
    return HttpResponse(jsonpickle.encode(network, unpicklable=False))
