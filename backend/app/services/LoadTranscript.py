from youtube_transcript_api import YouTubeTranscriptApi
import logging
import re
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class getYouTubeTranscript:
    def __init__(self, url):
        self.url = url
        self.videoID = self.parseURL(url)
        if not self.videoID:
            logger.error("Invalid YouTube URL: %s", url)
            raise ValueError("Invalid YouTube URL")
    
    @staticmethod
    def parseURL(url):
        pattern = (
            r'(?:https?:\/\/)?(?:www\.)?'
            r'(?:youtube\.com|youtu\.be)\/(?:watch\?v=|embed\/|v\/|.+\?v=)?'
            r'([^#&?\/]{11})'
        )
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return None
    
    def fetchTranscript(self):
        try:
            YTTAPI = YouTubeTranscriptApi()
            fetchedTranscript = YTTAPI.fetch(self.videoID)
            logger.info("Transcript fetched successfully for video ID: %s", self.videoID)
            return fetchedTranscript
        except Exception as e:
            logger.error("Error fetching transcript using YouTubeTranscriptApi: %s", str(e))
            return None

    def getRawData(self):
        fetchedTranscript = self.fetchTranscript()
        return fetchedTranscript.to_raw_data()
    


class YoutubeTranscriptLoader:
    def __init__(self, url, chunkSizeSeconds=60, addVideoInfo=False):
        self.url = url
        self.chunkSizeSeconds = chunkSizeSeconds
        self.addVideoInfo = addVideoInfo
        try:
            self.loader = YoutubeLoader.from_youtube_url(
                url,
                add_video_info=addVideoInfo,
                transcript_format=TranscriptFormat.CHUNKS,
                chunk_size_seconds=chunkSizeSeconds,
            )
        except Exception as e:
            logger.error("Error initializing YoutubeLoader: %s", str(e))
            self.loader = None
        self.docs = None

    def load(self):
        if self.loader is None:
            logger.error("Loader not initialized")
            return []
        try:
            self.docs = self.loader.load()
            logger.info("Documents loaded successfully")
            return self.docs
        except Exception as e:
            logger.error("Error loading documents: %s", str(e))
            return []


    def getChunks(self):
        if self.docs is None:
            self.load()
        return self.docs


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=aircAruvnKk&t=1s&ab_channel=3Blue1Brown"

    YTTranscriptAPIloader = getYouTubeTranscript(url)
    transcript = YTTranscriptAPIloader.getRawData()
    if transcript:
        print("Transcript fetched successfully.")
    else:
        print("Failed to fetch transcript.")

    print(transcript)

    langchainTranscriptLoader = YoutubeTranscriptLoader(url)
    chunks = langchainTranscriptLoader.getChunks()
    if chunks:
        print("Chunks loaded successfully.")
        for chunk in chunks:
            print(chunk)
            