from django.test import TestCase
from django.test import Client
from django.urls import resolve


# Create your tests here.
class UrlsTest(TestCase):
    def test_dashboard(self):
        resolver = resolve('/dashboard/')
        self.assertEquals(resolver.view_name, 'dashboard')

    def test_job_meta(self):
        resolver = resolve('/dashboard/job-meta/')
        self.assertEquals(resolver.view_name, 'job_meta')

    def test_job_success_failure(self):
        resolver = resolve('/dashboard/job-success-failure/')
        self.assertEquals(resolver.view_name, 'job_success_failure_ratio')


class viewTest(TestCase):

    def test_secure_view(self):
        c = Client()
        response = c.get('/dashboard')
        self.assertEqual(response.status_code, 301)

