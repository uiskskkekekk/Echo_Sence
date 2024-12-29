import re

class Checker:
    youtube_regex = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$')
    
    @classmethod
    def is_yt_link(cls, yt_link: str):
        return cls.youtube_regex.match(yt_link) is not None