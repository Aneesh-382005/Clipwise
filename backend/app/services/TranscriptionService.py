import logging

class TranscriptionService:
    """
    To handle transcription of a video that tries all fallbacks:)
    """
    def __init__(self, url):
        self.url = url
        self.transcript = None
        self.transcription = None

    def TryYoutubeTranscriptAPI(self, url):
        try:
            try:
                from .TranscriptionLoaders import getYouTubeTranscript
            except ImportError:
                from backend.app.services.TranscriptionLoaders import getYouTubeTranscript
            
            YTTranscriptAPIloader = getYouTubeTranscript(url)
            transcript = YTTranscriptAPIloader.getRawData()
            if transcript:
                logging.info("Transcript fetched successfully using YouTubeTranscriptApi.")
                self.transcript = transcript
                self.transcription = {
                    'text': transcript['text'],
                    'data': transcript,
                    'method': 'YouTubeTranscriptApi',
                    'success': True,
                    'error': ''
                }
                return self.transcription
                
        except Exception as e:
            logging.error(f"Error fetching transcript using YouTubeTranscriptApi: {e}. Trying the Langchain loader.")

    def TryLangchainLoader(self, url):    
        try:
            try:
                from backend.app.services.TranscriptionLoaders import YoutubeTranscriptLoader
            except ImportError:
                from .TranscriptionLoaders import YoutubeTranscriptLoader        
            
            try:
                langchainTranscriptLoader = YoutubeTranscriptLoader(url)
                chunks = langchainTranscriptLoader.getChunks()
                if chunks:
                    logging.info("Transcript fetched successfully using Langchain loader.")
                    combinedText = ' '.join([chunk.page_content for chunk in chunks])
                    self.transcription = {
                        'text': combinedText,
                        'data': chunks,
                        'method': 'Langchain',
                        'success': True,
                        'error': ''
                    }
                    return self.transcription
            except Exception as e:
                logging.error(f"Error loading chunks with Langchain: {e}")
        except Exception as e:
            logging.error(f"Error loading transcript using Langchain: {e}. Trying the Groq Whisper transcriber.")

    def TryGroqWhisperTranscriber(self, url):    
        try:
            try:
                from backend.app.services.getWhisperTranscriptions import WhisperTranscriber
            except ImportError:
                from .getWhisperTranscriptions import WhisperTranscriber
            
            transcriber = WhisperTranscriber()
            transcript = transcriber.transcribeFromURL(url)
            if transcript:
                logging.info("Transcription fetched successfully using Whisper.")
                self.transcription = {
                    'text': transcript['text'],
                    'data': transcript,
                    'method': 'Whisper',
                    'success': True,
                    'error': ''
                }
                return self.transcription
        except Exception as e:
            logging.error(f"Error fetching transcription using Whisper: {e}")
    
    def transcribe(self):
        """
        Tries to transcribe the video using various methods in order of preference.
        """
        self.TryYoutubeTranscriptAPI(self.url)
        if self.transcription and self.transcription['success']:
            return self.transcription
        
        self.TryLangchainLoader(self.url)
        if self.transcription and self.transcription['success']:
            return self.transcription
        
        self.TryGroqWhisperTranscriber(self.url)
        if self.transcription and self.transcription['success']:
            return self.transcription
        
        logging.error("All methods failed to fetch a transcript.")
        return {
            'text': '',
            'data': None,
            'method': '',
            'success': False,
            'error': 'All methods failed to fetch a transcript.'
        }
