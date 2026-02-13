import sys
import os
import yt_dlp
from moviepy import VideoFileClip
from pydub import AudioSegment

# ---------------------- VALIDATION ----------------------

def validate_inputs():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Error: NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    if num_videos <= 10:
        print("Error: NumberOfVideos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("Error: AudioDuration must be greater than 20 seconds.")
        sys.exit(1)

    output_file = sys.argv[4]

    return singer, num_videos, duration, output_file


# ---------------------- DOWNLOAD ----------------------

def download_videos(singer, num):
    print("Downloading videos...")

    os.makedirs("videos", exist_ok=True)

    search_query = f"ytsearch{num}:{singer} songs"

    ydl_opts = {
    'format': 'mp4',
    'outtmpl': 'videos/%(id)s.%(ext)s',
    'quiet': True,
    'socket_timeout': 60,
    'retries': 10,
    'fragment_retries': 10
}


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

    print("Download completed.")


# ---------------------- CONVERT TO AUDIO ----------------------

def convert_to_audio():
    print("Converting videos to audio...")

    os.makedirs("audios", exist_ok=True)

    for file in os.listdir("videos"):
        video_path = os.path.join("videos", file)
        audio_path = os.path.join("audios", file.split('.')[0] + ".mp3")

        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)
        clip.close()

    print("Conversion completed.")


# ---------------------- TRIM AUDIO ----------------------

def trim_audio(duration):
    print("Trimming audio files...")

    os.makedirs("trimmed", exist_ok=True)

    for file in os.listdir("audios"):
        audio_path = os.path.join("audios", file)
        trimmed_path = os.path.join("trimmed", file)

        audio = AudioSegment.from_mp3(audio_path)
        trimmed = audio[:duration * 1000]
        trimmed.export(trimmed_path, format="mp3")

    print("Trimming completed.")


# ---------------------- MERGE AUDIO ----------------------

def merge_audio(output_file):
    print("Merging audio files...")

    combined = AudioSegment.empty()

    for file in os.listdir("trimmed"):
        audio_path = os.path.join("trimmed", file)
        audio = AudioSegment.from_mp3(audio_path)
        combined += audio

    combined.export(output_file, format="mp3")

    print(f"Mashup created successfully: {output_file}")


# ---------------------- MAIN ----------------------

def main():
    try:
        singer, num_videos, duration, output_file = validate_inputs()

        download_videos(singer, num_videos)
        convert_to_audio()
        trim_audio(duration)
        merge_audio(output_file)

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    main()
