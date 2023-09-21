import pypdf

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
            return ''.join([pdf_reader.pages[x].extract_text() for x in range(len(pdf_reader.pages))]), pdf_reader.metadata
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
