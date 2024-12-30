from django.test import TestCase
from django.urls import reverse
from Music.models import Category, Artist, Music
from django.utils.http import urlencode
from Feature.extractor import FeatureExtractor
from rest_framework.test import APITestCase
from unittest.mock import patch
import json

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class AddMusicTest(TestCase):
    def setUp(self):
        # 創建測試類別
        category = Category.objects.create(name="Rock")
        artist = Artist.objects.create(name="Artist A", url="https://example.com/artist_a")


    @patch('Music.views.requests.post')  # 模擬 requests.post
    @patch('Feature.views.get_feature')  # 模擬 Feature.views.get_feature
    def test_add_music(self, mock_get_info, mock_post):
        urls = [
            "https://www.youtube.com/watch?v=4VkWsBukAWI",
            "https://www.youtube.com/watch?v=7JJfJgyHYwU",
            "https://www.youtube.com/watch?v=hT_nvWreIhg",
        ]

        # 設定 mock_get_info 的返回值
        mock_get_info.return_value.status_code = 200
        mock_get_info.return_value.json.return_value = {
            "data": [
                0.0, 0.41767391562461853, 0.0, 0.0, 1.0,
                0.990570068359375, 0.0, 0.7353748679161072,
                0.30306562781333923, 0.994108259677887
            ],
            "stringified_data": "0.0,0.41767391562461853,0.0,0.0,1.0,0.990570068359375,0.0,0.7353748679161072,0.30306562781333923,0.994108259677887"
        }

        # 設定 mock_post 的返回值
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": [
                0.0, 0.41767391562461853, 0.0, 0.0, 1.0,
                0.990570068359375, 0.0, 0.7353748679161072,
                0.30306562781333923, 0.994108259677887
            ],
            "stringified_data": "0.0,0.41767391562461853,0.0,0.0,1.0,0.990570068359375,0.0,0.7353748679161072,0.30306562781333923,0.994108259677887"
        }

        for url in urls:
            data = {"yt_link": url}

            # 發送 POST 請求到 'upload_music'
            response = self.client.post(reverse('upload_music'), data=data, format='json')

            print(response.json())

        data = {'target_id': 1}

        top10 = self.client.post(reverse('get_similiar_musics'), data=data)
        print(top10.json())
        
