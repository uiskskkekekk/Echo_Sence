from django.urls import reverse
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse,
)
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from Music.models import Artist, Music
from Music.similiarity import MusicSimilarityComparator
from uuid import uuid4
import logging
import requests
import json

msc = MusicSimilarityComparator()

logger = logging.getLogger("Feature")


@csrf_exempt
def upload_music(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    yt_link = request.POST.get("yt_link")

    if yt_link is None:
        return JsonResponse({"error": "The 'yt_link' field is missing."}, status=400)

    data = {"yt_link": yt_link}

    url = request.build_absolute_uri(reverse("info"))
    response = requests.post(url, data=data)
    info = response.json()
    id = info.get("id")

    music = Music.get_music_from_id(id)
    if music is not None:
        return JsonResponse({"data": music.music_id})

    url = request.build_absolute_uri(reverse("feature"))
    response = requests.post(url, data=data)
    features = response.json().get("data")

    try:
        music_id = Music.upload_music(info=info, features=features)
        if music_id is None:
            return JsonResponse(
                {"error": "Music upload failed due to an unknown error."}, status=500
            )
        return JsonResponse({"data": music_id})
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse(
            {"error": "Unknown error.", "error_id": error_id}, status=500
        )


@csrf_exempt
def get_similiar_musics(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    yt_link = request.POST.get("yt_link")
    data = {"yt_link": yt_link}

    url = request.build_absolute_uri(reverse("info"))
    response = requests.post(url, data=data)
    info = response.json()
    id = info.get("id")

    music = Music.get_music_from_id(id)
    if music is None:
        return JsonResponse({"error": "Music has not been uploaded."}, status=500)

    try:
        res = msc.compare(music.get("music_id"))
        if res is None:
            return JsonResponse(
                {
                    "error": "Music similarity comparison failed due to an unknown error."
                },
                status=500,
            )
        return JsonResponse({"original_data": music, "data": res})
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse(
            {"error": "Unknown error.", "error_id": error_id}, status=500
        )


@csrf_exempt
def test_create_data(request):
    artist = Artist.objects.create(
        artist_id="@123", name="Artist A", url="https://example.com/artist_a"
    )

    return HttpResponse("ok")
