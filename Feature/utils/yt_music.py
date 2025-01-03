import yt_dlp
import os
from pydub import AudioSegment
from pydub.utils import which
from datetime import datetime
import logging

AudioSegment.converter = which("ffmpeg") 

logger = logging.getLogger("Feature")

# https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#embedding-examples

class Downloader:
    download_range = [30.0, 60.0]
    no_warnings = True
    no_progress = True
    no_playlist = True
    
    download_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'paths': {
            'home': ""
        },
        'outtmpl': {
            'default': '%(id)s.%(ext)s'
        },
        'quite': True,
        'download_ranges': yt_dlp.utils.download_range_func(
            [], 
            [download_range]
        ),
        'no_warnings': no_warnings,
        'no_progress': no_progress,
        'noplaylist': no_playlist
    }
    
    @classmethod
    def download(cls, url, to=None, quiet=False):
        home = './data/music/temp' if to is None else os.path.join(to, "temp")
        cls.download_opts['paths']['home'] = home
        cls.download_opts['quiet'] = quiet
        try:
            with yt_dlp.YoutubeDL(cls.download_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                logger.info("Downloading music...")
                logger.info(f"Title: {info.get('title')}")
                filepath = ydl.prepare_filename(info, outtmpl=cls.download_opts['outtmpl']['default'])
                abspath = os.path.abspath(filepath)
                if to is None:
                    to = os.path.dirname(abspath)
                return cls.m4a_to_mp3(abspath, to)
        except Exception as e:
            raise e
            
    @classmethod
    def m4a_to_mp3(cls, input_file: str, output_path: str=None):
        if output_path is None:
            output_path = os.path.abspath("./data/music/download")
        logger.info("Transform .m4a file to .mp3 file...")
        audio = AudioSegment.from_file(input_file, format="m4a")
        
        filename = os.path.basename(input_file).removesuffix(".m4a") + ".mp3"
        output_path = os.path.join(output_path, filename)
        
        audio.export(output_path, format="mp3")
        logger.info(f"Output path: {os.path.abspath(output_path)}")
        os.remove(input_file)
        logger.info(f"Remove file: {os.path.abspath(output_path)}")
        return output_path
    
    @classmethod
    def get_info(cls, yt_link: str):
        opts = {
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
            'quiet': True,
            'noplaylist': cls.no_playlist
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(yt_link, False)
                return cls._get_music_info(info)
        except Exception as e:
            raise e
        
    @classmethod
    def get_full_data(cls, url, to=None, quiet=False):
        home = './data/music/temp' if to is None else os.path.join(to, "temp")
        cls.download_opts['paths']['home'] = home
        cls.download_opts['quiet'] = quiet
        try:
            with yt_dlp.YoutubeDL(cls.download_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                logger.info("Downloading music...")
                logger.info(f"Title: {info.get('title')}")
                filepath = ydl.prepare_filename(info, outtmpl=cls.download_opts['outtmpl']['default'])
                abspath = os.path.abspath(filepath)
                if to is None:
                    to = os.path.dirname(abspath)
                return {
                    "output_path": cls.m4a_to_mp3(abspath, to),
                    "info": cls._get_music_info(info)
                }
        except Exception as e:
            raise e
        
    @classmethod
    def _get_music_info(cls, info: dict):
        # https://github.com/ytdl-org/youtube-dl?tab=readme-ov-file#output-template
        video_id = info.get("id")
        ts = info.get("timestamp")
        dt = datetime.fromtimestamp(ts) if ts is not None else None
        return dict({
            "id": video_id,
            "title": info.get("title"),
            "author_id": info.get("uploader_id"),
            "author": info.get("uploader"),
            "youtube_url": f"https://www.youtube.com/watch?v={video_id}" if video_id is not None else None,
            "preview_url": info.get("url"),
            "cover_url": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
            "upload_time": dt,
            "upload_timestamp": info.get("timestamp"),
            "view_count": info.get("view_count"),
            "like_count": info.get("like_count")
        })
        

        
if __name__ == "__main__":
    # download("https://www.youtube.com/watch?v=t3kOeUsnocg")
    while True:
        try:
            Downloader.download(input("URL: "))
        except:
            break