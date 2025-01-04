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
            
        
main("https://www.youtube.com/watch?v=bB3-CUMERIU&list=PLO7-VO1D0_6MXmcpkq6zDLZB9h57H01KL&index=5")