"""
Integration tests relating to the API views
"""

from django.test import Client, TransactionTestCase
from api.models import JobType, Job
from django.http import JsonResponse


class ApiViewsTest(TransactionTestCase):

    def setUp(self):
        self.client = Client()

        job_type = JobType.objects.create(description='LINKEDIN')
        job_type.save()

        job = Job(user_id=10, status='running', type=job_type)
        job.save()

    '''
    Test that an 400 returned if incorrect data sent
    '''
    def test_run_linkedin_throw_exception(self):
        response = self.client.post('/api/v1/linkedin', {})

        self.assertEqual(400, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_run_linkedin_post(self):
        payload = '{"username": "someusername", "password": "somepassword", "user_id": 1}'

        response = self.client.post('/api/v1/linkedin', payload, content_type='text/plain;charset=UTF-8')

        self.assertEqual(200, response.status_code)

        # Test job was created in db
        response = self.client.get('/api/v1/job/1')
        self.assertEqual(200, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_run_linkedin_GET_fails(self):
        response = self.client.get('/api/v1/linkedin')

        self.assertEqual(500, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_get_job_by_id_404(self):
        response = self.client.get('/api/v1/job/201')

        self.assertEqual(404, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_get_job_by_id_POST_fails(self):
        response = self.client.post('/api/v1/job/201')

        self.assertEqual(500, response.status_code)

    def test_get_job_by_id(self):
        response = self.client.get('/api/v1/job/1')

        self.assertEqual(200, response.status_code)

    def test_get_job_by_user_id_POST_fails(self):
        response = self.client.post('/api/v1/job/user/10')

        self.assertEqual(500, response.status_code)

    def test_get_job_by_user_id(self):
        response = self.client.get('/api/v1/job/user/10')

        self.assertEqual(200, response.status_code)






