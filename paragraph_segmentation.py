import yaml
from sentence_transformers import SentenceTransformer
from utils.utilities import replace_newlines
import spacy
from get_config import Config
import numpy as np
import re

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
        doc = self.nlp (content)
        #Set p=s1. Now compare p and s2. If they are similar, p=p+s2. Continue until p#s(n)
        previous_sentence = None
        current_length = 0
        paragraph = ''
        paragraphs = []
        for sentence in doc.sents:
            tokens = len(self.nlp(sentence.text))
            cleaned_sentence = re.sub(pattern='\n+', repl=' ', string=sentence.text)   
            #cleaned_sentence = replace_newlines(cleaned_sentence)
      
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
                    paragraphs.append(paragraph)
                    paragraph=cleaned_sentence
                    previous_sentence = None
                    current_length = 0
            else:
                if(current_length+tokens < self.chunk_size):
                    paragraph = cleaned_sentence
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
    paragraphs = ParagraphSegmenter().create_paragraph("This is ia sentence. And this is another one. The end")
    for paragraph in paragraphs:
        print(paragraph)

