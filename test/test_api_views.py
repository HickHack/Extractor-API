import django
import os
from django.test import Client, utils, TestCase
from api.models import JobType
from django.http import JsonResponse


class ApiViewsTest(TestCase):

    def setUp(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extractor_api.settings")
        django.setup()
        utils.setup_test_environment()
        self.client = Client()

        # Create JobTypes
        type1 = JobType(description='LINKEDIN')
        type1.save()

    def test_run_linkedin_throw_exception(self):
        response = self.client.post('/api/v1/linkedin', {})

        self.assertEqual(400, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_run_linkedin_post(self):
        payload = '{"username": "someusername", "password": "somepassword"}'
        response = self.client.post('/api/v1/linkedin', payload, content_type='text/plain;charset=UTF-8')

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)

        # Test job was created in db
        response = self.client.get('/api/v1/job/1')
        self.assertEqual(200, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))

    def test_run_linkedin_GET_fails(self):
        response = self.client.get('/api/v1/linkedin')

        self.assertEqual(500, response.status_code)
        self.assertTrue(isinstance(response, JsonResponse))






