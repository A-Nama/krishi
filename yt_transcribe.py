import yt_dlp
import whisper

video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

# Step 1: Download audio only
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "audio.%(ext)s",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

# Step 2: Transcribe with Whisper
model = whisper.load_model("medium")  # can use "large" for better accuracy
result = model.transcribe("audio.mp3", language="ml")

with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])
