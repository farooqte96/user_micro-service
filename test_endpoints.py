from unittest import TestCase

import requests


class TestFlaskApiUsingRequests(TestCase):
    def test_login(self):
        response = requests.get('http://127.0.0.1:5000/customers')
        self.assertEqual(response.status_code, 200)

