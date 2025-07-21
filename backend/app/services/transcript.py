from youtube_transcript_api import YouTubeTranscriptApi
import re
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat

class getYouTubeTranscript:
    def __init__(self, url):
        self.url = url
        self.videoID = self.parseURL(url)
        if not self.videoID:
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
        YTTAPI = YouTubeTranscriptApi()
        fetchedTranscript = YTTAPI.fetch(self.videoID)
        return fetchedTranscript
    
    def getRawData(self):
        fetchedTranscript = self.fetchTranscript()
        return fetchedTranscript.to_raw_data()
    
    def getTranscriptText(self):
        fetchedTranscript = self.fetchTranscript()
        for snippet in fetchedTranscript:
            print(snippet.text)


class YoutubeTranscriptLoader:
    def __init__(self, url, chunkSizeSeconds=60, addVideoInfo=False):
        self.url = url
        self.chunkSizeSeconds = chunkSizeSeconds
        self.addVideoInfo = addVideoInfo
        self.loader = YoutubeLoader.from_youtube_url(
            url,
            add_video_info=addVideoInfo,
            transcript_format=TranscriptFormat.CHUNKS,
            chunk_size_seconds=chunkSizeSeconds,
        )
        self.docs = None

    def load(self):
        self.docs = self.loader.load()
        return self.docs

    def getChunks(self):
        if self.docs is None:
            self.load()
        return self.docs
