"""
API Controller unit tests
"""

import mock
import api.controllers as controllers
from django.test import TestCase
from api.utils import ResponseTemplate


class TestAPIControllers(TestCase):

    @mock.patch('api.controllers.Job')
    @mock.patch('api.controllers.JobType')
    @mock.patch('api.controllers.Thread')
    def test_process_linkedin_run(self, mock_thread, mock_job_type, mock_job):
        result = controllers.process_linkedin_run('username', 'password', 'user_id')

        self.assertTrue(mock_thread.called)
        self.assertTrue(mock_job.called)
        self.assertTrue(isinstance(result, ResponseTemplate))
        self.assertTrue(result.jobs)
        mock_job_type.objects.get.called_with(1)

    @mock.patch('api.controllers.Job')
    def test_process_get_job_by_id(self, mock_job):
        result = controllers.process_get_job_by_id(1)

        mock_job.obejects.get.called_with(1)
        self.assertTrue(isinstance(result, ResponseTemplate))
        self.assertTrue(result.jobs)

    @mock.patch('api.controllers.Job')
    def test_process_get_job_by_user_id(self, mock_job):
        result = controllers.process_get_job_by_user_id(1)

        mock_job.objects.all.filter.called_with(1)
        self.assertTrue(isinstance(result, ResponseTemplate))
        self.assertFalse(result.jobs)




