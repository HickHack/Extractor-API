from api.views import LinkedInView, TwitterView, JobsView
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^linkedin$', LinkedInView.as_view(), name='linkedin'),
    url(r'^twitter$', TwitterView.as_view(), name='twitter'),
    url(r'^job/(?P<pk>[0-9]+)$', JobsView.as_view({'get': 'get_by_id'})),
    url(r'^job/user/(?P<user_id>[0-9]+)$', JobsView.as_view({'get': 'get_by_user_id'}), name='jobs_by_user'),
    url(r'^job/user/(?P<user_id>[0-9]+)/summary', JobsView.as_view({'get': 'get_summary'}), name='jobs_by_user_summary'),
    url(r'^endpoints$', JobsView.as_view({'get': 'publish_endpoints'})),
    url(r'^api-token-auth$', obtain_jwt_token, name='obtain_auth_token'),
    url(r'^api-token-refresh$', refresh_jwt_token, name='api_token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
