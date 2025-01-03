from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
import logging
import json

from .extractor import FeatureExtractor
from .utils.check_helper import Checker
from .utils.yt_music import Downloader

fe = FeatureExtractor(
    encoder_path = "static/feature/models/best.h5",
    runtime_dir = "static/feature/runtime"
)

logger = logging.getLogger("Feature")

FIELD_ERROR_NO = 400
UNSUPPORT_METHOD_ERROR_NO = 405
UNKNOWN_ERROR_NO = 500

@csrf_exempt
def get_feature(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=UNSUPPORT_METHOD_ERROR_NO)
    
    if not fe.is_loaded: 
        return JsonResponse(
            {"error": "The model could not be loaded. Please check the file path or model file integrity."},
            status=UNKNOWN_ERROR_NO
        )
    
    yt_link = request.POST.get("yt_link")
    if yt_link is None: 
        return JsonResponse({"error": "The 'yt_link' field is missing."}, status=FIELD_ERROR_NO)
    
    if not Checker.is_yt_link(yt_link): 
        return JsonResponse({"error": "The 'yt_link' field must be a valid YouTube link."}, status=FIELD_ERROR_NO)
    
    try:
        res = fe.extract(yt_link)
        if res is None:
            return JsonResponse({"error": "Feature extraction failed due to an unknown error."}, status=UNKNOWN_ERROR_NO)
        res = res.tolist()
        return JsonResponse({
            "data": res,
            "stringified_data": ",".join(map(str, res))
        })
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse({"error": "Unknown error.", "error_id": error_id}, status=UNKNOWN_ERROR_NO)

@csrf_exempt
def get_info(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=UNSUPPORT_METHOD_ERROR_NO)
    
    yt_link = request.POST.get("yt_link")
    if not yt_link:
        return JsonResponse({"error": "The 'yt_link' field is required."}, status=FIELD_ERROR_NO)
    
    if not Checker.is_yt_link(yt_link):
        return JsonResponse({"error": "The 'yt_link' field must be a valid Youtube link."}, status=FIELD_ERROR_NO)
    
    try:
        info = Downloader.get_info(yt_link)
        if info is None:
            return JsonResponse({"error": "Get info failed due to an unknown error."}, status=UNKNOWN_ERROR_NO)
        return JsonResponse(info)
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse({"error": "Unknown error.", "error_id": error_id}, status=UNKNOWN_ERROR_NO)
    
@csrf_exempt
def get_full_data(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=UNSUPPORT_METHOD_ERROR_NO)
    
    if not fe.is_loaded: 
        return JsonResponse(
            {"error": "The model could not be loaded. Please check the file path or model file integrity."},
            status=UNKNOWN_ERROR_NO
        )
    
    yt_link = request.POST.get("yt_link")
    if not yt_link:
        return JsonResponse({"error": "The 'yt_link' field is required."}, status=FIELD_ERROR_NO)
    
    if not Checker.is_yt_link(yt_link):
        return JsonResponse({"error": "The 'yt_link' field must be a valid Youtube link."}, status=FIELD_ERROR_NO)
    
    try:
        res = Downloader.get_full_data(yt_link, quiet=True)
        output_path = res.get("output_path")
        info = res.get("info")
        
        if res is None or output_path is None or info is None:
            return JsonResponse({"error": "Get info failed due to an unknown error."}, status=UNKNOWN_ERROR_NO)
        
        feature = fe.extract_from_file(output_path)
        if feature is None:
            return JsonResponse({"error": "Feature extraction failed due to an unknown error."}, status=UNKNOWN_ERROR_NO)
        
        feature = feature.tolist()
        return JsonResponse({
            "feature": {
                "data": feature,
                "stringified_data": ",".join(map(str, res))
            },
            "info": info
        })
    except Exception as e:
        error_id = uuid4()
        logger.error(f"{str(e)} ({error_id})")
        return JsonResponse({"error": "Unknown error.", "error_id": error_id}, status=UNKNOWN_ERROR_NO)