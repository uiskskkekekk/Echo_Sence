import yt_dlp
import json

opts = {
    'extract_flat': 'in_playlist',
    'fragment_retries': 10,
    'ignoreerrors': 'only_download',
    'noprogress': True,
    'postprocessors': [{
        'key': 'FFmpegConcat',
        'only_multi_video': True,
        'when': 'playlist'
    }],
    'quiet': True,
    'retries': 10,
    'simulate': True
}

def main(url):
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        entries = info.get("entries")
        
        res = [{"yt_link": entry.get("url")} for entry in entries]
            
        with open(f"{info.get('id')}.json", "w", encoding="utf8") as jfile:
            json.dump(res, jfile, ensure_ascii=False, indent=4)
            
        
main("https://www.youtube.com/playlist?list=PL2Uevv7vJzCNisIYcr63D9-tASVSzDP-O")