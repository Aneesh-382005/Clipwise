from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

url = "https://www.youtube.com/watch?v=aircAruvnKk&t=1s&ab_channel=3Blue1Brown"

yt = YouTube(url, on_progress_callback = on_progress)
videoTitle = yt.title
print(videoTitle)

path = "backend/app/utilities/downloads"
os.makedirs(path, exist_ok=True)

ys = yt.streams.get_highest_resolution()
ys.download(output_path = path, filename = videoTitle + ".mp4")

audioOnly = yt.streams.get_audio_only()
audioOnly.download(output_path = path, filename = videoTitle + ".m4a")