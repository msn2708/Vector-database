import pypdf
import json
import spacy
import re

class FileParser:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            print(f"Exception in loading spacy library: {e.with_traceback()}")
            
    def parse(self, file_path):
        raise NotImplementedError("Subclasses must implement the 'parse' method")
        
    def clean(self, content):
        # Split the content into sentences
        page_paragraphs = content.split('\n')
                    
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
    def clean(self, content):
        return super().clean(content)
    
    def extract_metadata(self, metadata):
        if metadata:
            # Extract metadata
                if "/Keywords" in metadata:
                    keywords = metadata["/Keywords"]
                else:
                    keywords = ''
                
                if metadata.author:
                    author=metadata['/Author']
                else: 
                    author = ''
                
                if "/Creator" in metadata:
                    creator=metadata['/Creator']
                else: 
                    creator=''
                    
                if metadata.subject:
                    subject=metadata['/Subject']
                else:
                    subject = ''
                
                if metadata.title:
                    title=metadata['/Title']
                else:
                    title=''
                    
                if metadata.creation_date_raw:
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
                return json.loads(metadata_json)
            
    def parse(self, file_path):
        try:
            paragraphs = []
            metadata_dict = {}
            
            # PDF parsing logic here
            pdf_file = open(file_path, 'rb')
            pdf_reader = pypdf.PdfReader(pdf_file)            
            # printing number of pages in pdf file
            print(f"Total number of pages in {file_path}", len(pdf_reader.pages))
            
            if pdf_reader.metadata:
                metadata_dict = self.extract_metadata(pdf_reader.metadata)
               
            #extract text from the pdf file
            content = ''.join([pdf_reader.pages[x].extract_text() for x in range(len(pdf_reader.pages))])
                
            #clean the content
            content = self.clean(content)
            
            return content, metadata_dict, paragraphs    
        except Exception as e: 
            print(f"Error {e} trying to parse file {file_path}")
        finally:
            # closing the pdf file object
            pdf_file.close()
            

class DocxParser(FileParser):
    def parse(self, file_path):
        # DOCX parsing logic here
        pass

class HtmlParser(FileParser):
    def parse(self, file_path):
        # HTML parsing logic here
        pass
            
