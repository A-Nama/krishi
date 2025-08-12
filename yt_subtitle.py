import yt_dlp

video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

ydl_opts = {
    "writesubtitles": True,       # write subtitles
    "writeautomaticsub": True,    # auto-generated if official subs not available
    "subtitleslangs": ["ml"],     # 'ml' = Malayalam
    "skip_download": True,        # only download subs, not video
    "outtmpl": "%(title)s.%(ext)s"
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
