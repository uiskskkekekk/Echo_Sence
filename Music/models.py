from django.db import models
from django.db.models import Manager

class Artist(models.Model):
    artist_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'artist'

    @classmethod
    def create_artist(cls, artist_id: str, name: str):
        artist = cls.objects.create(
            artist_id = artist_id,
            name=name, 
            url=f"https://www.youtube.com/{artist_id}"
        )

        return artist

    @classmethod
    def get_artist(cls, artist_id: str) -> Manager["Artist"]:
        return cls.objects.filter(artist_id=artist_id)

class Music(models.Model):
    music_id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=20, blank=True, null=True)
    rating = models.IntegerField(default=0, null=True)
    outer_url = models.URLField(max_length=500, blank=True, null=True)
    rating_count = models.IntegerField(default=0)
    listen_count = models.IntegerField(default=0)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    features = models.JSONField()
    
    class Meta:
        managed = True
        db_table = 'music'

    @classmethod
    def upload_music(cls, music_id, info, features):
        author_id = info.get('author_id')
        author = info.get('author')
        title = info.get('title')
        youtube_url = info.get('youtube_url')

        artist = Artist.get_artist(author_id).first()
        if artist is None: artist = Artist.create_artist(author_id, author)
            
        music = cls.objects.create(
            music_id = music_id,
            title = title,
            outer_url = youtube_url,
            artist = artist,
            features = features
        )

        return music.music_id
    
    @classmethod
    def check_exists(cls, music_id):
        return cls.objects.filter(music_id=music_id).exists()