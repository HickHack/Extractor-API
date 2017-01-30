from django.test import Client, TestCase
from api.models import JobType
from django.http import JsonResponse


class ApiViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_run_linkedin_throw_exception(self):
        response = self.client.post('/api/v1/linkedin', {})

        self.assertEqual(400, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_run_linkedin_post(self):
        job_type = JobType.objects.create(description='LINKEDIN')
        job_type.refresh_from_db()

        payload = '{"username": "someusername", "password": "somepassword"}'
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






