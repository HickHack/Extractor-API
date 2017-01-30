"""
Tests for API models to ensure they are
correctly
"""

from django.test import TransactionTestCase
from api.models import Job, JobType


class TestAPIModels(TransactionTestCase):

    def test_all_correctly_persisted(self):
        job_type = JobType(description='LINKEDIN')
        job_type.save()

        job = Job(user_id=12, status='running',
                  type=job_type, start_time=1234,
                  end_time=3456, complete=True)

        job.save()

        self.assertEqual('LINKEDIN', job_type.description)

        self.assertEqual(12, job.user_id)
        self.assertEqual('running', job.status)
        self.assertEqual(job_type.id, job.type.id)
        self.assertEqual(1234, job.start_time)
        self.assertEqual(3456, job.end_time)
        self.assertTrue(job.complete)

    def test_all_correctly_persisted_default_values(self):
        job_type = JobType(description='LINKEDIN')
        job_type.save()

        job = Job(user_id=12, status='running',
                  type=job_type)

        job.save()

        self.assertEqual(0, job.start_time)
        self.assertEqual(0, job.end_time)
        self.assertFalse(job.complete)