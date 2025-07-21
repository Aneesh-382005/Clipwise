from youtube_transcript_api import YouTubeTranscriptApi
import re

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
