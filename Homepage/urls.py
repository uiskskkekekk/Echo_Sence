from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirect_homepage, name="redirect_to_homepage"),
    path("homepage/", views.index, name="homepage"),
]