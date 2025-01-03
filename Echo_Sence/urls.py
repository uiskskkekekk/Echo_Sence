from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('feature',include('Feature.urls')),
    path('music', include('Music.urls')),
    path("", include("Homepage.urls")),
    path("upload/", include("Upload.urls")),
    path("analyze/", include("Analyze.urls")),
]