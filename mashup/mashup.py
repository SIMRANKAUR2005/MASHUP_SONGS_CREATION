import os
import yt_dlp
from moviepy import VideoFileClip
from pydub import AudioSegment

def create_mashup(singer, num_videos, duration, output_file):

    os.makedirs("videos", exist_ok=True)
    os.makedirs("audios", exist_ok=True)
    os.makedirs("trimmed", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # Download
    search_query = f"ytsearch{num}:{singer} official songs audio"

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'videos/%(id)s.%(ext)s',
    'quiet': True,
    'noplaylist': True,
    'ignoreerrors': True,
    'default_search': 'ytsearch',
    'extract_flat': False,
    'source_address': '0.0.0.0'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

    # Convert
    for file in os.listdir("videos"):
        video_path = os.path.join("videos", file)
        audio_path = os.path.join("audios", file.split('.')[0] + ".mp3")

        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)
        clip.close()

    # Trim
    for file in os.listdir("audios"):
        audio = AudioSegment.from_mp3(os.path.join("audios", file))
        trimmed = audio[:duration * 1000]
        trimmed.export(os.path.join("trimmed", file), format="mp3")

    # Merge
    combined = AudioSegment.empty()

    for file in os.listdir("trimmed"):
        audio = AudioSegment.from_mp3(os.path.join("trimmed", file))
        combined += audio

    output_path = os.path.join("output", output_file)
    combined.export(output_path, format="mp3")

    return output_path