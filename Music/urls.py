from django.urls import path
from . import views

urlpatterns = [
    path('/upload_music', views.upload_music, name='upload_music'),
    path('/get_similiar_musics', views.get_similiar_musics, name='get_similiar_musics'),
    path('/test_create_data', views.test_create_data, name='test_create_data'),
]