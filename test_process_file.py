from tika import parser
import mysql.connector
import mariadb
from get_config import get_config
from sqlescapy import sqlescape

    
def insert_into_db():
    #input each of these paragraphs into a DB
    
    # Connect to the MariaDB database
    config = get_config()
    db_config = config.get('db_config')
    try:

        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        
        select_query = "SELECT * FROM document"
        result = cursor.execute(select_query)
        if result:
          rows = cursor.fetchall()
          for row in rows:
            print(row)
          
        # Insert data into a table
        insert_query = "INSERT INTO vectordb.document (file_name, `text`, doc_type) VALUES (%s, %s, %s)"
        doc_row = ('a.txt', 'lousy text, skdfhkkjkjdf kdjfhkjsd ,,,\n', 'application/pdf')
        print(doc_row)
        
        try:
          cursor.execute(insert_query,doc_row)
          if(cursor.rowcount == 0):
            print("something failed")
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
  insert_into_db ()
  