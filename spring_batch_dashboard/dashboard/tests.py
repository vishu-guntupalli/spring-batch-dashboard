from django.test import TestCase
from django.test import Client


# Create your tests here.

class viewTest(TestCase):

    def test_views(self):
        c = Client()
        response = c.get('/dashboard')
        self.assertEqual(response.status_code, 200)

