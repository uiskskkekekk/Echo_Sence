from django.db import models
from django.db.models import Manager
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'category'

    @classmethod
    def get_category(cls, category_id: int):
        return cls.objects.get(category_id=category_id)

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'artist'

    @classmethod
    def get_category(cls, artist_id: int):
        return cls.objects.get(artist_id=artist_id)

class Music(models.Model):
    music_id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=20, blank=True, null=True)
    rating = models.IntegerField(default=0, null=True)
    outer_url = models.URLField(max_length=500, blank=True, null=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating_count = models.IntegerField(default=0)
    listen_count = models.IntegerField(default=0)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    features = models.JSONField()
    
    class Meta:
        managed = True
        db_table = 'music'

    @classmethod
    def upload_music(cls, music_id, title, outer_url, category_id, artist_id, features):
        category = Category.get_category(category_id=1)
        artist = Artist.get_category(artist_id=1)

        music = cls.objects.create(
            music_id = music_id,
            title = title,
            outer_url = outer_url,
            category_id = category,
            artist_id = artist,
            features = features
        )

        return music.music_id
    
    @classmethod
    def check_exists(cls, music_id):
        return cls.objects.filter(music_id=music_id).exists()