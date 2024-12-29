import yt_dlp
import os
from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = which("ffmpeg") 

# https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#embedding-examples

class Downloader:
    @classmethod
    def download(cls, url, to=None, quiet=False):
        home = './data/music/temp' if to is None else os.path.join(to, "temp")
        opts = {
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
            'paths': {
                'home': home
            },
            'outtmpl': {
                'default': '%(id)s.%(ext)s'
            },
            'quiet': quiet
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                print("Title:", info.get("title"))
                filepath = ydl.prepare_filename(info, outtmpl=opts['outtmpl']['default'])
                abspath = os.path.abspath(filepath)
                if to is None:
                    to = abspath
                return cls.m4a_to_mp3(abspath, to)
        except:
            pass
        return None
            
    @classmethod
    def m4a_to_mp3(cls, input_file: str, output_path: str=None):
        audio = AudioSegment.from_file(input_file, format="m4a")
        
        if output_path is None:
            output_path = os.path.abspath("./data/music/download")
        filename = os.path.basename(input_file).removesuffix(".m4a") + ".mp3"
        
        output_path = os.path.join(output_path, filename)
        
        audio.export(output_path, format="mp3")
        print(f"[output] {output_path}")
        os.remove(input_file)
        return output_path
    
    @classmethod
    def get_info(cls, yt_link: str):
        opts = {
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
            'quiet': True
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            # https://github.com/ytdl-org/youtube-dl?tab=readme-ov-file#output-template
            info = ydl.extract_info(yt_link, False)
            return {
                "title": info.get("title"),
                "author": info.get("uploader")
            }
        return None
        

        
if __name__ == "__main__":
    # download("https://www.youtube.com/watch?v=t3kOeUsnocg")
    while True:
        try:
            Downloader.download(input("URL: "))
        except:
            break