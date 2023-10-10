import sys
from tika import parser
from get_config import Config
from parser_factory import FileParserFactory
from orm_models import Document
import utils.utilities as utils
from write_chunks_to_queue import write_chunks_to_queue
from text_processor_exception import TextProcessingError as tpe
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Function to process each file
def process_file(filename):
  if not(utils.is_file_exists(filename) and utils.is_file_readable(filename)):
    raise tpe(f"file {filename} is either not readable or does not exist",logging.ERROR)
  
  config = Config().get_config()

  try:
    parsed_file = parser.from_file(filename)
    doc_type = parsed_file["metadata"]["Content-Type"]
    ret_parser = FileParserFactory.create_parser(filename, doc_type)
    
    if ret_parser is not None:
      ret_parser.parse()
      content = ret_parser.clean()
      metadata = ret_parser.extract_metadata(parsed_file['metadata'])
    else:
      content = parsed_file['content']
      metadata = parsed_file['metadata']
    
    document = Document(file_name=filename, doc_type=doc_type, text=content)
    document.create_chunks()
    document.create_metadata(metadata=metadata)
    engine = create_engine(config.get('db_url'))
    _session = sessionmaker(engine)
    with _session() as session:  
      session.add(document)
      session.commit()
      if(config['write-chunks-to-queue'] == True):
        for chunk in document.chunks:
          write_chunks_to_queue(chunk)
  except Exception as e:
    raise tpe(f"Error during session save : {e.with_traceback()}", logging.ERROR)

if __name__ == '__main__':
  process_file(sys.argv[1])
  