import os
import logging
from pytubefix import YouTube
from pytubefix.cli import on_progress

class MediaDownloader:
    def __init__(self, url, downloadPath="backend/app/utilities/downloads"):
        self.url = url
        self.downloadPath = downloadPath
        os.makedirs(self.downloadPath, exist_ok=True)

        logger = logging.getLogger("MediaDownloaderLogger")
        if not logger.hasHandlers():
            logger.setLevel(logging.INFO)
            fileHandler = logging.FileHandler(os.path.join(self.downloadPath, "mediaDownloader.log"))
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
        self.logger = logger

    def download(self):
        try:
            yt = YouTube(self.url, on_progress_callback = on_progress)
            videoTitle = yt.title
            self.logger.info(f"Starting download for: {videoTitle}")

            try:
                ys = yt.streams.get_highest_resolution()
                videoFile = os.path.join(self.downloadPath, f"{videoTitle}.mp4")
                ys.download(output_path = self.downloadPath, filename=f"{videoTitle}.mp4")
                self.logger.info(f"Video downloaded: {videoFile}")
            except Exception as e:
                self.logger.error(f"Video download failed: {e}")

            try:
                audio_only = yt.streams.get_audio_only()
                audioFile = os.path.join(self.downloadPath, f"{videoTitle}.m4a")
                audio_only.download(output_path=self.downloadPath, filename=f"{videoTitle}.m4a")
                self.logger.info(f"Audio downloaded: {audioFile}")
            except Exception as e:
                self.logger.error(f"Audio download failed: {e}")

        except Exception as e:
            self.logger.error(f"Failed to initialize YouTube object: {e}")
    
    def downloadAudio(self):
        """Download only audio and return the file path"""
        try:
            yt = YouTube(self.url, on_progress_callback=on_progress)
            videoTitle = self.sanitizeFilename(yt.title)
            self.logger.info(f"Downloading audio for: {videoTitle}")
            audioStream = yt.streams.get_audio_only()
            if not audioStream:
                raise Exception("No audio stream available")
            
            filename = f"{videoTitle}.m4a"
            filePath = os.path.join(self.downloadPath, filename)

            audioStream.download(output_path=self.downloadPath, filename=filename)
            self.logger.info(f"Audio downloaded: {filePath}")

            return filePath
        
        except Exception as e:
            self.logger.error(f"Audio download failed: {e}")
            raise e
        
    def getVideoInfo(self):
        """Get video metadata without downloading"""
        try:
            yt = YouTube(self.url)
            return {
                "title": yt.title,
                "description": yt.description,
                "duration": yt.length,
                "views": yt.views,
                "author": yt.author,
                "publish_date": yt.publish_date,
                "videoID": yt.video_id
            }
        except Exception as e:
            self.logger.error(f"Failed to get video info: {e}")
            return None

    def sanitizeFilename(self, filename):
        """Remove invalid characters from filename"""
        invalid_chars = r'<>:"/\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        return filename.strip()

if __name__ == "__main__":
    downloader = MediaDownloader("https://www.youtube.com/watch?v=aircAruvnKk&t=1s&ab_channel=3Blue1Brown")
    downloader.download()
