"""
Integration tests relating to the API views
"""

from django.test import Client, TransactionTestCase
from api.models import JobType, Job
from django.contrib.auth.models import User
from django.http import JsonResponse
from random import randint


class ApiViewsTest(TransactionTestCase):

    def setUp(self):
        self.client = Client()

        job_type = JobType.objects.create(description='LINKEDIN')
        job_type.save()

        job = Job(user_id=10, status='running', type=job_type)
        job.save()

        self.header = {'HTTP_AUTHORIZATION': 'Bearer ' + self.get_auth_token()}

    '''
    Test that an 400 returned if incorrect data sent
    '''
    def test_run_linkedin_throw_exception(self):
        response = self.client.post('/api/v1/linkedin', {}, **self.header)

        self.assertEqual(400, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_run_linkedin_post(self):
        payload = '{"username": "someusername", "password": "somepassword", "user_id": 1}'

        response = self.client.post('/api/v1/linkedin', payload, content_type='text/plain;charset=UTF-8', **self.header)

        self.assertEqual(200, response.status_code)

        # Test job was created in db
        response = self.client.get('/api/v1/job/1', **self.header)
        self.assertEqual(200, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_run_linkedin_GET_fails(self):
        response = self.client.get('/api/v1/linkedin', **self.header)

        self.assertEqual(405, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_run_linkedin_auth_401(self):
        response = self.client.post('/api/v1/linkedin', {})

        self.assertEqual(401, response.status_code)

    def test_get_job_by_id_404(self):
        response = self.client.get('/api/v1/job/201', **self.header)

        self.assertEqual(404, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_get_job_by_id_POST_fails(self):
        response = self.client.post('/api/v1/job/201', **self.header)

        self.assertEqual(405, response.status_code)

    def test_get_job_by_id(self):
        response = self.client.get('/api/v1/job/1', **self.header)

        self.assertEqual(200, response.status_code)

    def test_get_job_by_id_auth_401(self):
        response = self.client.get('/api/v1/job/1')

        self.assertEqual(401, response.status_code)

    def test_get_job_by_user_id_POST_fails(self):
        response = self.client.post('/api/v1/job/user/10', **self.header)

        self.assertEqual(405, response.status_code)

    def test_get_job_by_user_id(self):
        response = self.client.get('/api/v1/job/user/10', **self.header)

        self.assertEqual(200, response.status_code)

    def test_get_job_by_user_id_auth_401(self):
        response = self.client.get('/api/v1/job/user/10')

        self.assertEqual(401, response.status_code)

    def get_auth_token(self):
        user = User.objects.create_user(username=str(randint(50, 1000)), password='123456',
                                        email='test@exograph.com', is_staff=True, is_superuser=True)
        user.save()

        response = self.client.post('/api/v1/api-token-auth',
                                 {"username": user.username, "password": '123456'})

        if response.status_code == 200:
            return response.data['token']







