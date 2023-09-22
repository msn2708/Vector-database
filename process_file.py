import multiprocessing
import os
from tika import parser
#import mysql.connector
import mariadb
from get_config import Config
from create_embedding import get_embedding
from sqlescapy import sqlescape
from parser_factory import FileParserFactory
from models import Document, Metadata, Chunk
from get_paragraphs import get_paragraphs
from session_factory import SessionFactory
import re
import sys

# Function to process each file
def process_file(filename):
  paragraphs = []
  try:
    parsed_file = parser.from_file(filename)
    doc_type = parsed_file["metadata"]["Content-Type"]
    if doc_type == 'application/pdf':
      try:
        pdf_parser = FileParserFactory.create_parser(filename)
        content, metadata = pdf_parser.parse(filename)
      except Exception as e:
        print(f"Error parsing PDF file {filename}: {e}")
    else:
      content = parsed_file['content']
      metadata = parsed_file['metadata']
      
    paragraphs = get_paragraphs(content)
    
    """
    document = Document(file_name=filename, doc_type=doc_type, text=content)
    document.create_chunks()
    document.create_metadata(metadata=metadata)
    
    session = SessionFactory().get_session().begin()
    session.add(document)
    session.commit()
    """
    insert_into_db(filename=filename,metadata=metadata,paragraphs=paragraphs,doctype=doc_type,config=Config().get_config())
  except Exception as e:
    print(f"Error: {e}")
    
def insert_into_db(filename,metadata,paragraphs,doctype,config):
    #input each of these paragraphs into a DB
    
    # Connect to the MariaDB database
    db_config = config.get('db_config')
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
                
        # Insert data into a table
        insert_query = "INSERT INTO vectordb.document (file_name, `text`, doc_type) VALUES (%s, %s, %s)"
        doc_row = (filename, sqlescape(''.join(paragraphs).replace('\n\n','\n').replace('\n','').strip()), doctype)
        
        try:
          cursor.execute(insert_query,doc_row)
          document_id = cursor.lastrowid
          
          if(cursor.rowcount == 0):
            print("something failed")
        except mariadb.Error as e:
          print(f"SQL Error while inserting DOCUMENT: {e.sqlstate}: {e.msg}")
        for paragraph in paragraphs:
          chunk_query = "INSERT INTO vectordb.chunk (document_id, text, embedding) VALUES (%s, %s, %s)"
          chunk_row = (document_id, paragraph, get_embedding(paragraph))
          try:
            cursor.execute(chunk_query, chunk_row)
          except mariadb.Error as e:
            print(f"SQL Error while inserting CHUNK: {e.sqlstate}: {e.msg}")
            
        for key,value in metadata:
          chunk_query = "INSERT INTO vectordb.chunk (document_id, key, value) VALUES (%s, %s, %s)"
          chunk_row = (document_id, key, value)
          try:
            cursor.execute(chunk_query, chunk_row)
          except mariadb.Error as e:
            print(f"SQL Error while inserting into METADATA: {e.sqlstate}: {e.msg}")

        # Commit the transaction
        conn.commit()

    except Exception as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and the database connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
  process_file(sys.argv[1])
  