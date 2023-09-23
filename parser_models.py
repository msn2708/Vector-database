import pypdf
import json

class FileParser:
    def parse(self, file_path):
        raise NotImplementedError("Subclasses must implement the 'parse' method")

class PdfParser(FileParser):
    def parse(self, file_path):
        try:
            # PDF parsing logic here
            pdf_file = open(file_path, 'rb')
            pdf_reader = pypdf.PdfReader(pdf_file)            
            # printing number of pages in pdf file
            print("Total number of pages in sample.pdf", len(pdf_reader.pages))
            #write a for loop to iterate over the pages
            if pdf_reader.metadata:
                # Extract metadata
                if "/Keywords" in pdf_reader.metadata:
                    keywords = pdf_reader.metadata["/Keywords"].resolve()
                    print(keywords)
                else:
                    keywords = ''
                
                if pdf_reader.metadata.author:
                    author=pdf_reader.metadata['/Author'].resolve().decode('utf-8').replace('\n', '')
                else: 
                    author = ''
                
                if "/Creator" in pdf_reader.metadata.creator:
                    creator=pdf_reader.metadata['/Creator'].resolve()[0].decode('utf-8').replace('\n','')
                else: 
                    creator=''
                    
                if pdf_reader.metadata.subject:
                    subject=pdf_reader.metadata['/Subject'].resolve()
                else:
                    subject = ''
                
                if pdf_reader.metadata.title:
                    title=pdf_reader.metadata['/Title']
                else:
                    title=''
                    
                if pdf_reader.metadata.creation_date_raw:
                    creation_date_raw=pdf_reader.metadata['/CreationDate']
                else:
                    creation_date_raw=''
                    
                metadata = {
                    'author': author,
                    'creator': creator,
                    'subject': subject,
                    'title': title,
                    'keywords': keywords,
                    'creation_date': creation_date_raw
                }
                metadata_json = json.dumps(metadata)
                metadata_dict = json.loads(metadata_json)
                
            return ''.join([pdf_reader.pages[x].extract_text() for x in range(len(pdf_reader.pages))]), metadata_dict
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
