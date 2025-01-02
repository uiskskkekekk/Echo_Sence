from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from Music.models import Category,Artist, Music
from Music.similiarity import MusicSimilarityComparator
from uuid import uuid4
import logging
import requests

msc = MusicSimilarityComparator()

logger = logging.getLogger("Feature")

@csrf_exempt
def upload_music(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    yt_link = request.POST.get('yt_link')

    if yt_link is None:
        return JsonResponse({"error": "The 'yt_link' field is missing."}, status=400)
    
    data = {"yt_link": yt_link}
    
    url = request.build_absolute_uri(reverse('full'))
    response = requests.post(url, data=data)
    resp_data = response.json()

    features = resp_data.get('feature').get('data')
    info = resp_data.get('info')
    id = info.get('id')
    title = info.get('title')
    print(title)

    if Music.check_exists(id): return JsonResponse({"data": id})

    try:
        res = Music.upload_music(music_id=id, title=title, outer_url=yt_link, category_id=1, artist_id=1, features=features)
        if res is None:
            return JsonResponse({"error": "Music upload failed due to an unknown error."}, status=500)
        return JsonResponse({"data": res})
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse({"error": "Unknown error.", "error_id": error_id}, status=500)
    
@csrf_exempt   
def get_similiar_musics(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    yt_link = request.POST.get("yt_link")
    print(yt_link)
    data = {"yt_link": yt_link}
    url = request.build_absolute_uri(reverse('full'))
    response = requests.post(url, data=data)
    resp_data = response.json()

    
    info = resp_data.get('info')
    id = info.get("id")

    try:
        res = msc.compare(id)
        if res is None:
            return JsonResponse({"error": "Music similarity comparison failed due to an unknown error."}, status=500)
        return JsonResponse({"data": res, "info": info})
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse({"error": "Unknown error.", "error_id": error_id}, status=500)

@csrf_exempt
def test_create_data(request):
    category = Category.objects.create(name="Rock")
    artist = Artist.objects.create(name="Artist A", url="https://example.com/artist_a")

    return HttpResponse('ok')