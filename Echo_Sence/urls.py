from django.urls import path, include
from . import views

urlpatterns = [
    path('feature/',include('Feature.urls')),
    path('', views.index, name='index'),
]