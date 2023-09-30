import multiprocessing
import os
from tika import parser
from get_config import Config
from create_embedding import get_embedding
from sqlescapy import sqlescape
from parser_factory import FileParserFactory
from orm_models import Document, Metadata, Chunk
from get_paragraphs import get_paragraphs
import sys
from utils.utilities import *
from write_chunks_to_queue import write_chunks_to_queue

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Function to process each file
def process_file(filename):
  if not(is_file_exists(filename) and is_file_readable(filename)):
    print(f"file {filename} is either not readable or does not exist")
    return # something more meaningful
  try:
    parsed_file = parser.from_file(filename)
    doc_type = parsed_file["metadata"]["Content-Type"]
    if doc_type == 'application/pdf':
      try:
        pdf_parser = FileParserFactory.create_parser(filename)
        content, metadata, paragraphs = pdf_parser.parse(filename)
      except Exception as e:
        print(f"Error parsing PDF file {filename}: {e}")
    elif doc_type == 'application/text':
      content=parsed_file['content']
      metadata={}
    else:
      content = parsed_file['content']
      metadata = parsed_file['metadata']    
    
    document = Document(file_name=filename, doc_type=doc_type, text=content)
    document.create_chunks()
    document.create_metadata(metadata=metadata)
    
    engine = create_engine(Config().get_config().get('db_url'))
    Session = sessionmaker(engine)
    with Session() as session:  
      session.add(document)
      session.commit()
      for chunk in document.chunks:
        write_chunks_to_queue(chunk)
  except Exception as e:
    print(f"Error during session save : {e.with_traceback()}")

if __name__ == '__main__':
  process_file(sys.argv[1])
  