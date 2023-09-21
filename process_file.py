import multiprocessing
import os
from tika import parser
import mysql.connector
import mariadb
from get_config import get_config
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

    
    document = Document(file_name=filename, doc_type=doc_type, text=content)
    document.create_chunks()
    document.create_metadata(metadata=metadata)
    
    session = SessionFactory().get_session().begin()
    session.add(document)
    session.commit()
    
    #insert_into_db(parsed_file,config)
  except Exception as e:
    print(f"Error: {e}")
    
def insert_into_db(parsed_file,config):
    #input each of these paragraphs into a DB
    
    # Connect to the MariaDB database
    db_config = config.get('db_config')
    try:
        paragraphs = get_paragraphs(parsed_file['content'])

        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
                
        # Insert data into a table
        insert_query = "INSERT INTO vectordb.document (file_name, `text`, doc_type) VALUES (%s, %s, %s)"
        doc_row = (parsed_file["metadata"]["resourceName"], sqlescape(''.join(paragraphs).replace('\n\n','\n').replace('\n','').strip()), parsed_file["metadata"]["Content-Type"])
        
        try:
          cursor.execute(insert_query,doc_row)
          document_id = cursor.lastrowid
          
          if(cursor.rowcount == 0):
            print("something failed")
        except mariadb.Error as e:
          print(f"SQL Error: {e.sqlstate}: {e.msg}")
        for paragraph in paragraphs:
          chunk_query = "INSERT INTO vectordb.chunk (document_id, text, embedding) VALUES (%s, %s, %s)" 
          chunk_row = (document_id, paragraph, '')
          try:
            cursor.execute(chunk_query, chunk_row)
          except mariadb.Error as e:
            print(f"SQL Error: {e.sqlstate}: {e.msg}")

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
  