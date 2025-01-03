from django.db import models
from django.db.models import Manager
from django.forms.models import model_to_dict

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
        return cls.objects.filter(artist_id=artist_id).first()

class Music(models.Model):
    music_id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=20, blank=True, null=True)
    youtube_url = models.URLField(max_length=500, blank=True, null=True)
    cover_url = models.URLField(max_length=500, blank=True, null=True)
    preview_url = models.URLField(max_length=1000, blank=True, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    features = models.JSONField()
    
    class Meta:
        managed = True
        db_table = 'music'

    @classmethod
    def upload_music(cls, info, features):
        music_id = info.get('id')
        author_id = info.get('author_id')
        author = info.get('author')
        title = info.get('title')
        youtube_url = info.get('youtube_url')
        cover_url = info.get('cover_url')
        preview_url = info.get('preview_url')
        view_count = info.get('view_count')
        like_count = info.get('like_count')

        artist = Artist.get_artist(author_id)
        if artist is None: artist = Artist.create_artist(author_id, author)
            
        music = cls.objects.create(
            music_id = music_id,
            title = title,
            youtube_url = youtube_url,
            cover_url = cover_url,
            preview_url = preview_url,
            artist = artist,
            view_count = view_count,
            like_count = like_count,
            features = features
        )

        music_artist = cls.get_music_from_id(music_id)
        return music_artist
    
    @classmethod
    def get_music_from_id(cls, music_id):
        music = cls.objects.select_related('artist').filter(music_id=music_id)
        music_data = music.values('music_id', 'title', 'youtube_url', 'cover_url', 'preview_url', 'artist_id', 'artist__name', 'view_count', 'like_count', 'features').first()
        formatted_data = {
            'music_id': music_data.get('music_id'),
            'title': music_data.get('title'),
            'youtube_url': music_data.get('youtube_url'),
            'cover_url': music_data.get('cover_url'),
            'preview_url': music_data.get('preview_url'),
            'artist_id': music_data.get('artist_id'),
            'artist_name': music_data.get('artist__name'),
            'view_count': music_data.get('view_count'),
            'like_count': music_data.get('like_count'),
            'features': music_data.get('features'),
        }

        return formatted_data
    
    @classmethod
    def get_all_music_exclude_id(cls, music_id):
        music = cls.objects.select_related('artist').exclude(music_id=music_id)
        music_data = music.values('music_id', 'title', 'youtube_url', 'cover_url', 'preview_url', 'artist_id', 'artist__name', 'view_count', 'like_count', 'features')
        formatted_data = [
            {
                'music_id': item.get('music_id'),
                'title': item.get('title'),
                'youtube_url': item.get('youtube_url'),
                'cover_url': item.get('cover_url'),
                'preview_url': item.get('preview_url'),
                'artist_id': item.get('artist_id'),
                'artist_name': item.get('artist__name'),
                'view_count': item.get('view_count'),
                'like_count': item.get('like_count'),
                'features': item.get('features'),
            }
            for item in music_data
        ]

        return formatted_data