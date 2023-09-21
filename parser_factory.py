from parser_models import PdfParser, DocxParser, HtmlParser, FileParser
class FileParserFactory:
    @staticmethod
    def create_parser(filename):
            
        file_extension = filename.split('.')[-1].lower()

        if file_extension == 'pdf':
            return PdfParser()
        elif file_extension == 'docx':
            return DocxParser()
        elif file_extension == 'html':
            return HtmlParser()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
