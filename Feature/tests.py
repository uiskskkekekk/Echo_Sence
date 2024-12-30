from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
import json

class FeatureTestCase(APITestCase):
    def test_get_feature(self):
        data = {"yt_link": "https://www.youtube.com/watch?v=slvejIelzio"}
        resp = self.client.post("/feature", data)
        resp_data = json.loads(resp.content)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('data', resp_data)
        
    def test_get_info(self):
        data = {"yt_link": "https://www.youtube.com/watch?v=slvejIelzio"}
        resp = self.client.post("/feature/info", data)
        resp_data = json.loads(resp.content)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('id', resp_data)
    
    def test_get_feature_with_wrong_url(self):
        data = {"yt_link": "https://www.youtube.com/watch?v=slvejIelzia"}
        resp = self.client.post("/feature", data)
        
        self.assertEqual(resp.status_code, 500)
        
    def test_get_info_with_wrong_url(self):
        data = {"yt_link": "https://www.youtube.com/watch?v=slvejIelzia"}
        resp = self.client.post("/feature/info", data)
        
        self.assertEqual(resp.status_code, 500)