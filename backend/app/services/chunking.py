#This is a class for chunking a document into semantic chunks.
#We use Greg Kamradt's semantic chunking algorithm to split the document into sentences.

import re
import logging
from langchain_openai.embeddings import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

class SemanticChunking:
    def __init__(self, document):
        self.document = document

    def split_into_sentences(self):
        singleSentencesList = re.split(r'(?<=[.?!])\s+', self.document)
        logging.info(f"Number of sentences split: {len(singleSentencesList)}")
        sentences = [{'sentence': x, 'index': i} for i, x in enumerate(singleSentencesList)]
        return sentences

    def combine_sentences(self, sentences, buffer_size=1):
        for i in range(len(sentences)):
            combined_sentence = ''
            for j in range(i - buffer_size, i):
                if j >= 0:
                    combined_sentence += sentences[j]['sentence'] + ' '
            combined_sentence += sentences[i]['sentence']
            for j in range(i + 1, i + 1 + buffer_size):
                if j < len(sentences):
                    combined_sentence += ' ' + sentences[j]['sentence']
            sentences[i]['combined_sentence'] = combined_sentence
        return sentences

    def add_embeddings(self, sentences, oaiembeds):
        embeddings = oaiembeds.embed_documents([x['combined_sentence'] for x in sentences])
        for i, sentence in enumerate(sentences):
            sentence['combined_sentence_embedding'] = embeddings[i]
        return sentences

    def calculate_cosine_distances(self, sentences):
        distances = []
        for i in range(len(sentences) - 1):
            embedding_current = sentences[i]['combined_sentence_embedding']
            embedding_next = sentences[i + 1]['combined_sentence_embedding']
            similarity = cosine_similarity([embedding_current], [embedding_next])[0][0]
            distance = 1 - similarity
            distances.append(distance)
            sentences[i]['distance_to_next'] = distance
        return distances, sentences

    def get_breakpoints(self, distances, percentile=95):
        breakpoint_distance_threshold = np.percentile(distances, percentile)
        indices_above_thresh = [i for i, x in enumerate(distances) if x > breakpoint_distance_threshold]
        return indices_above_thresh, breakpoint_distance_threshold

    def chunk_sentences(self, sentences, indices_above_thresh):
        chunks = []
        start_index = 0
        for index in indices_above_thresh:
            end_index = index
            group = sentences[start_index:end_index + 1]
            combined_text = ' '.join([d['sentence'] for d in group])
            chunks.append(combined_text)
            start_index = index + 1
        if start_index < len(sentences):
            combined_text = ' '.join([d['sentence'] for d in sentences[start_index:]])
            chunks.append(combined_text)
        return chunks
    

    

    

#This is also a class for chunking a document into semantic chunks.
#We use LangChain's text splitter to split the document into chunks which is also taken from Greg Kamradt's semantic chunking algorithm.

from langchain_experimental.text_splitter import SemanticChunker
import numpy as np


class SemanticChunkingLangChain:
    '''
    Chunk a document into semantic chunks using LangChain's SemanticChunker.
    '''
    def __init__(
        self,
        breakpointThresholdType: str = "percentile",
        breakpointThresholdAmount: float = None,
        minChunkSize: int = None,
    ):
        '''
        Initialize with optional breakpoint and chunk size settings.
        '''
        kwargs = {"breakpoint_threshold_type": breakpointThresholdType}
        if breakpointThresholdAmount is not None:
            kwargs["breakpoint_threshold_amount"] = breakpointThresholdAmount
        if minChunkSize is not None:
            kwargs["min_chunk_size"] = minChunkSize

        self.textSplitter = SemanticChunker(OpenAIEmbeddings(), **kwargs)

    def createDocuments(self, texts):
        '''
        Split input texts into semantic chunks.
        '''
        return self.textSplitter.create_documents(texts)
