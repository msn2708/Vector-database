import pypdf
import json
import spacy
import re
from utils import utilities as utils
from text_processor_exception import TextProcessingError as tpe
import logging

class FileParser:
    def __init__(self,filepath):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.filepath = filepath
            self.content = ''
            self.metadata = {}            
        except Exception as e:
            print(f"Exception in loading spacy library: {e.with_traceback()}")
    
    def get_file_details(self):
        return self.content, self.metadata
      
    def parse(self):
        raise NotImplementedError("Subclasses must implement the 'parse' method")
    
    def extract_metadata(self, metadata):
        if metadata:
            # Extract metadata
                if "/Keywords" in metadata:
                    keywords = metadata["/Keywords"]
                else:
                    keywords = ''
                
                if "author" in metadata:
                    author=metadata['/Author']
                else: 
                    author = ''
                
                if "/Creator" in metadata:
                    creator=metadata['/Creator']
                else: 
                    creator=''
                    
                if "subject" in metadata:
                    subject=metadata['/Subject']
                else:
                    subject = ''
                
                if 'title' in metadata:
                    title=metadata['/Title']
                else:
                    title=''
                    
                if 'date' in metadata:
                    creation_date_raw= metadata['/CreationDate']
                else:
                    creation_date_raw=''
                    
                metadata_obj = {
                    'author': author,
                    'creator': creator,
                    'subject': subject,
                    'title': title,
                    'keywords': keywords,
                    'creation_date': creation_date_raw
                }
                metadata_json = json.dumps(metadata_obj)
                self.metadata = json.loads(metadata_json)
                return self.metadata
                            
    def clean(self, text_to_clean=''):
        if text_to_clean == '':
            # Split the content into sentences
            page_paragraphs = self.content.split('\n')
        else:
            page_paragraphs = text_to_clean.split('\n')
                    
        #remove any empty paragraphs
        cleaned_paragraphs = [paragraph.strip(' \t') for paragraph in page_paragraphs if paragraph.strip(' \t')]
                
        # split the paragraphs into sentences and delete any newlines, 
        # spaces and tabs in sentences.
        # Use Spacy to return an array of sentences from this paragraph
        for index, paragraph in enumerate(cleaned_paragraphs):
            doc = self.nlp (paragraph)
            cleaned_sentence = []
            for sent in doc.sents:
                cleaned = re.sub(pattern='\s+', repl=' ', string=sent.text)
                cleaned = re.sub(pattern='\n+', repl='\n', string=cleaned)
                cleaned = re.sub(pattern='\t+', repl='\t', string=cleaned)
                if (len(cleaned)>0):
                    cleaned_sentence.append(cleaned)
            page_paragraphs[index] = ''.join(cleaned_sentence)
        return '\n'.join(page_paragraphs)
        

class PdfParser(FileParser):
    def clean(self,text_to_clean=''):
        return super().clean()
    
    def extract_metadata(self, metadata):
        return super().extract_metadata(metadata=metadata)
            
    def parse(self):
        try:            
           # PDF parsing logic here
            pdf_file = open(self.filepath, 'rb')
            pdf_reader = pypdf.PdfReader(pdf_file)            
            # printing number of pages in pdf file
            print(f"Total number of pages in {self.filepath}", len(pdf_reader.pages))
            
            if pdf_reader.metadata:
                metadata_dict = self.extract_metadata(pdf_reader.metadata)
               
            #extract text from the pdf file
            self.content = ''.join([pdf_reader.pages[x].extract_text() for x in range(len(pdf_reader.pages))])
            
            #return content, metadata_dict, paragraphs
        except Exception as e: 
            print(f"Error {e} trying to parse file {self.filepath}")
        finally:
            # closing the pdf file object
            pdf_file.close()
            

class DocxParser(FileParser):
    def parse(self):
        # DOCX parsing logic here
        pass

class HtmlParser(FileParser):
    def parse(self):
        # HTML parsing logic here
        pass
    

class MovieParser(FileParser):
    def __init__(self, filepath):
        super().__init__(filepath)
        try:
            file=open(self.filepath, 'rb')
            if utils.is_file_exists(self.filepath) and utils.is_file_readable(self.filepath):
                self.content = file.read().decode('utf-8')         
        except Exception as e:
            raise tpe(f'Error processing movie corpus file: {e.with_traceback()}', logging.ERROR)
        finally:
            file.close()
        
    def get_content(self):
        return self.content
    
    def parse(self):
        try:
            patterns = r"--|FADE IN :|FADE OUT:|FADE IN:|FADE OUT :|CONTINUED:|DISSOLVE TO:|CUT TO:|POV|INT\.|EXT\.|\(CONT'D\)|\(V\.O\.\)|\(continuing\)|FADE IN\.|FADE OUT\.|\([^)]*\)"
            segments = re.split(patterns, self.content)
            chunks = [segment.strip() for segment in segments if segment.strip()]
            cleaned_chunks = []
            for chunk in chunks:
                cleaned_chunks.append(super().clean(chunk))
            self.content = '\n'.join(cleaned_chunks)                      
        except Exception as e:
            raise tpe(f'Error processing movie corpus file: {e.with_traceback()}', logging.ERROR)         
    
    def clean(self,text_to_clean=''):
        if text_to_clean == '':
            text = re.sub(pattern='\.+', repl='.', string=self.content)
            return super().clean(text)
        return super().clean(text_to_clean)