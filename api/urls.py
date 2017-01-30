from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^/linkedin$', views.linkedin_run, name='linkedin'),
    url(r'^/job/(?P<pk>[0-9]+)$', views.get_job_by_id, name='job'),
    url(r'^/job/user/(?P<user_id>[0-9]+)$', views.get_jobs_by_user_id, name='jobs_by_user'),
]