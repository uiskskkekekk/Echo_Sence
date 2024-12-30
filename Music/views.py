from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.http import HttpRequest
from django.test import RequestFactory
from Music.models import Category, Artist, Music
from Music.similiarity import MusicSimilarityComparator
from uuid import uuid4
import logging
import requests

msc = MusicSimilarityComparator()

logger = logging.getLogger("Music")

def upload_music(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    yt_link = request.POST.get('yt_link')

    if yt_link is None:
        return JsonResponse({"error": "The 'yt_link' field is missing."}, status=400)
    
    data = {"yt_link": yt_link}
    
    response = requests.post(reverse('feature'), data=data)

    resp_data = response.json()
    features = resp_data.get('data')

    try:
        res = Music.upload_music(title='testTitle', outer_url=yt_link, category_id=1, artist_id=1, features=features)
        if res is None:
            return JsonResponse({"error": "Music upload failed due to an unknown error."}, status=500)
        return JsonResponse({"data": res})
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse({"error": "Unknown error.", "error_id": error_id}, status=500)
    
def get_similiar_musics(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    target_id = request.POST.get("target_id")

    try:
        res = msc.compare(target_id)
        if res is None:
            return JsonResponse({"error": "Music similarity comparison failed due to an unknown error."}, status=500)
        return JsonResponse({"data": res})
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse({"error": "Unknown error.", "error_id": error_id}, status=500)

