from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
import logging

from .extractor import FeatureExtractor
from .utils.check_helper import Checker
from .utils.yt_music import Downloader

fe = FeatureExtractor(
    encoder_path = "static/feature/models/best.h5",
    runtime_dir = "static/feature/runtime"
)

logger = logging.getLogger("Feature")

@csrf_exempt
def get_feature(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)
    
    if not fe.is_loaded: 
        return JsonResponse(
            {"error": "The model could not be loaded. Please check the file path or model file integrity."},
            status=500
        )
    
    yt_link = request.POST.get("yt_link")
    if yt_link is None: 
        return JsonResponse({"error": "The 'yt_link' field is missing."}, status=400)
    
    if not Checker.is_yt_link(yt_link): 
        return JsonResponse({"error": "The 'yt_link' field must be a valid YouTube link."}, status=400)
    
    try:
        res = fe.extract(yt_link, format="str")
        if res is None:
            return JsonResponse({"error": "Feature extraction failed due to an unknown error."}, status=500)
        return JsonResponse({"result": res})
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse({"error": "Unknown error.", "error_id": error_id}, status=500)

@csrf_exempt
def get_info(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)
    
    yt_link = request.POST.get("yt_link")
    if not yt_link:
        return JsonResponse({"error": "The 'yt_link' field is required."}, status=400)
    
    if not Checker.is_yt_link(yt_link):
        return JsonResponse({"error": "The 'yt_link' field must be a valid Youtube link."}, status=400)
    
    try:
        info = Downloader.get_info(yt_link)
        return JsonResponse(info)
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse({"error": "Unknown error.", "error_id": error_id}, status=500)