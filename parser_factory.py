from parser_models import PdfParser, DocxParser, HtmlParser, FileParser, MovieParser
class FileParserFactory:
    @staticmethod
    def create_parser(filename, doctype):
        if 'application/pdf' in doctype:
            return PdfParser(filename)
        elif 'docx' in doctype:
            return DocxParser(filename)
        elif 'html' in doctype:
            return HtmlParser(filename)
        elif 'text/plain' in doctype:
            return MovieParser(filename)         
        else:
            return FileParser(filename)
        
