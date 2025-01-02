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

        self.mock_data = {
            "feature": {
                "data": [0.0,0.4453675448894501,0.0,0.0,0.9787300229072571,0.9661890864372253,0.0,0.7534757852554321,0.32637858390808105,1.0],
                "stringified_data": "output_path,info"
            },
            "info": {
                "id": "h_D3VFfhvs4",
                "title": "Michael Jackson - Smooth Criminal (Official Video)",
                "author_id": "@michaeljacksonVEVO",
                "author": "Michael Jackson",
                "youtube_url": "https://www.youtube.com/watch?v=h_D3VFfhvs4",
                "preview_url": "https://rr2---sn-o3iuf-3iie.googlevideo.com/videoplayback?expire=1735604752&ei=sOVyZ4qlMJXas8IPupz40Ag&ip=124.218.148.12&id=o-AJMR_720qVA6IqFR0iy5UiMwRhk2N-Y4qDEZclj2XtEM&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1735583152%2C&mh=hv&mm=31%2C29&mn=sn-o3iuf-3iie%2Csn-un57sne7&ms=au%2Crdu&mv=m&mvi=2&pl=24&rms=au%2Cau&pcm2=no&gcr=tw&initcwndbps=3918750&bui=AfMhrI-Sh4KSYKsDxiTWBtkT0eiID8Z9hyj3sr92ffiwNUbSDog2F2Kb5270v__ef-m8a5O7xRq4RtxR&spc=x-caULsBpedxv2jwmuI_fqfxk-6ssRlO3WmKR0RNCykIh5tbaKIN&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=9159522&dur=565.916&lmt=1716984503178045&mt=1735582646&fvip=1&keepalive=yes&fexp=51326932%2C51335594%2C51371294&c=IOS&txp=4532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cpcm2%2Cgcr%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRQIhAKtwVXuNun3JCEu9qJwxvwbM2-RJocSWs4SE4nJ0gxYHAiBGEScvppWXz6sTkYRNyKerHlfcjdk-8AO83h-nNcncxg%3D%3D&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIgSeHIaQYB8DPwlJZuNwEcIAA9MPNahpX4LwkwScQg7QICIQDUxmiRS-xtWRuCbpvs2LzVMrMCCV8KdVnQQb9eo4ef6g%3D%3D",
                "upload_time": "2010-11-19T19:39:43",
                "upload_timestamp": 1290166783,
                "view_count": 1027036602,
                "like_count": 10297936
            }
        }


    @patch('Music.views.requests.post')  # 模擬 requests.post
    @patch('Feature.views.get_full_data')  # 模擬 Feature.views.get_feature
    def test_add_music(self, mock_get_info, mock_post):
        urls = [
            "https://www.youtube.com/watch?v=4VkWsBukAWI",
            "https://www.youtube.com/watch?v=7JJfJgyHYwU",
            "https://www.youtube.com/watch?v=hT_nvWreIhg",
        ]

        # 設定 mock_get_info 的返回值
        mock_get_info.return_value.status_code = 200
        mock_get_info.return_value.json.return_value = self.mock_data

        # 設定 mock_post 的返回值
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.mock_data

        for url in urls:
            data = {"yt_link": url}

            # 發送 POST 請求到 'upload_music'
            response = self.client.post(reverse('upload_music'), data=data, format='json')

            print(response.json())

        data = {'target_id': 1}

        top10 = self.client.post(reverse('get_similiar_musics'), data=data)
        print(top10.json())
        
