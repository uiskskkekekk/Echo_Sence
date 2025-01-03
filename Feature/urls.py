from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_feature, name='feature'),
    path('/info', views.get_info, name='info'),
    path('/full', views.get_full_data, name='full')
]