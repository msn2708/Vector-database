from sentence_transformers import SentenceTransformer
from utils.utilities import replace_newlines
import spacy
from get_config import Config
import numpy as np
import re
from text_processor_exception import TextProcessingError
import logging
import sys


#this needs to be exposed as gRPC service
class ParagraphSegmenter():
    def __init__(self):
        self.config = Config().get_config()
        self.nlp = spacy.load("en_core_web_sm")
        self.sentence_encoder = SentenceTransformer('distiluse-base-multilingual-cased-v2')
        self.chunk_size = self.config['chunk_size']
        self.similarity_threshold = self.config['similarity_threshold']
        
    def cosine_similarity(self, sentence1, sentence2):
        dp = np.dot(sentence1,sentence2)
        norm_s1 = np.linalg.norm(sentence1)
        norm_s2 = np.linalg.norm(sentence2)
        return dp/(norm_s1*norm_s2)
    
    def create_paragraph(self, content):
        # Use Spacy to return an array of sentences from this corpus
        try:
            #doc = self.nlp (content)
            doc = re.split("\.",content)
        except Exception as e:
            raise TextProcessingError(f"ParagraphSegmenter: Unable to parse content. {e.__traceback__}", severity=logging.ERROR)
        #Set p=s1. Now compare p and s2. If they are similar, p=p+s2. Continue until p#s(n)
        previous_sentence = None
        current_length = 0
        paragraph = ''
        paragraphs = []
        short_words = []
        #for sentence in doc.sents:
        for sent in doc:
            sentence = sent
            if(len(sentence) < 25):
                short_words.append(re.sub(pattern='\n+', repl=' ', string=sentence))
                continue
            else:
                cleaned_sentence = (' '.join(short_words) + ' ' + sentence).strip()
                cleaned_sentence = re.sub(pattern='\n+', repl=' ', string=cleaned_sentence)
                cleaned_sentence = re.sub(pattern='\s+', repl=' ', string=cleaned_sentence)
                cleaned_sentence = re.sub(pattern='\.+', repl=".", string=cleaned_sentence)
                short_words = []
    
            tokens = len(self.nlp(cleaned_sentence))
                   
            current_sentence = self.sentence_encoder.encode(cleaned_sentence)
            
            similarity = 1
            if previous_sentence is not None:
                similarity = self.cosine_similarity(previous_sentence, current_sentence)
                if(current_length+tokens < self.chunk_size) and (similarity > self.similarity_threshold):
                    paragraph = paragraph.strip() + '. ' + cleaned_sentence
                    current_length += tokens
                    previous_sentence = current_sentence
                else:
                    #paragraph.strip()
                    paragraphs.append(paragraph + '. ')
                    paragraph=cleaned_sentence
                    previous_sentence = current_sentence
                    current_length = 0
            else:
                if(current_length+tokens < self.chunk_size):
                    paragraph = cleaned_sentence.strip()
                    current_length += tokens
                else:
                    print(f"Sentence too big for encoding: {cleaned_sentence}")
                    current_length=0
                    continue #what if the text size is bigger than what the model can encode?
                previous_sentence = current_sentence
        paragraphs.append(paragraph.strip())
        return paragraphs
                
                
    
#create a main program to invoke
if __name__ == "__main__":
    #open a file and read its contents
    with open(sys.argv[1], mode="r",encoding="utf-8") as f:        
        paragraphs = ParagraphSegmenter().create_paragraph(f.read())
        for paragraph in paragraphs:
            print(paragraph)

