from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest, HttpResponse, HttpResponseServerError, JsonResponse

from .extractor import FeatureExtractor
from .utils.check_helper import Checker
from .utils.yt_music import Downloader
import json

fe = FeatureExtractor(
    encoder_path = "static/feature/models/best.h5",
    runtime_dir = "static/feature/runtime"
)

def get_feature(request: HttpRequest):
    if not fe.is_loaded: 
        return HttpResponseBadRequest("The model could not be loaded. Please check the file path or model file integrity.")
    
    yt_link = request.POST.get("yt_link")
    if yt_link is None: return HttpResponseBadRequest("The 'yt_link' field is missing.")
    if not Checker.is_yt_link(yt_link): return HttpResponseBadRequest("The 'yt_link' field must be a valid Youtube link.")
    
    # yt_link = "https://www.youtube.com/watch?v=slvejIelzio" # test
    try:
        res = fe.extract(yt_link, format="str")
    except:
        return HttpResponseServerError("Unknown error.")
    
    if res is None: return HttpResponseServerError("Unknown error.")
    return HttpResponse(res)

def get_info(request: HttpRequest):
    info = Downloader.get_info("https://www.youtube.com/watch?v=slvejIelzio")
    print(info)
    return JsonResponse(json.dumps(info, indent=4), safe=False)