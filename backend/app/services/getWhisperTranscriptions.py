import os
import json
import logging
from groq import Groq
from dotenv import load_dotenv

try:
    from ..utilities.mediaDownloader import MediaDownloader
except ImportError:
    from backend.app.utilities.mediaDownloader import MediaDownloader

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class WhisperTranscriber:
    def __init__(self, model="whisper-large-v3-turbo", temperature=0.0):
        self.client = Groq()
        self.model = model
        self.temperature = temperature

    def transcribe(self, filepath):
        logging.info(f"Transcribing file: {filepath}")
        try:
            with open(filepath, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file = file,
                    model = self.model,
                    temperature = self.temperature
                )
            logging.info("Transcription successful.")
            return transcription
        except Exception as e:
            logging.error(f"Transcription failed: {e}")
            return None
    
    def transcribeFromURL(self, YTURL, cleanup = True):
        """Download audio from YouTube URL and transcribe it"""
        downloader = MediaDownloader(YTURL)
        downloader.logger.info(f"Starting transcription workflow for URL: {YTURL}")

        
        try:
            audioFile = downloader.downloadAudio()
            downloader.logger.info(f"Audio ready for transcription: {audioFile}")

            logging.info(f"Starting Whisper transcription for: {os.path.basename(audioFile)}")
            transcription = self.transcribe(audioFile)
            
            if cleanup and os.path.exists(audioFile):
                os.remove(audioFile)
                downloader.logger.info(f"Cleaned up temporary audio file: {audioFile}")

            return transcription
        except Exception as e:
            downloader.logger.error(f"Transcription workflow failed: {e}")
            return None

if __name__ == "__main__":
    # Example usage
    transcriber = WhisperTranscriber()
    YTURL = "https://www.youtube.com/watch?v=aircAruvnKk&t=1s&ab_channel=3Blue1Brown"
    result = transcriber.transcribeFromURL(YTURL)
    if result:
        print(json.dumps(result, indent=2, default=str))
    else:
        print("Transcription failed. See logs for details.")
        