import mysql.connector
from mysql.connector import errorcode
import mariadb

class DocumentPersister:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Access denied.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist.")
            else:
                print(f"Error: {err}")
            raise

    def persist_document(self, document):
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()

        try:
            # Insert the Document
            cursor.execute(
                "INSERT INTO document (doc_type, text) VALUES (%s, %s)",
                (document.doc_type, document.text)
            )
            document_id = cursor.lastrowid

            # Insert Metadata objects
            for metadata in document.metadata:
                cursor.execute(
                    "INSERT INTO metadata (document_id, key, value) VALUES (%s, %s, %s)",
                    (document_id, metadata.key, metadata.value)
                )

            # Insert Chunk objects
            for chunk in document.chunks:
                cursor.execute(
                    "INSERT INTO chunk (document_id, content) VALUES (%s, %s)",
                    (document_id, chunk.content)
                )

            # Commit the transaction
            self.connection.commit()
        except mysql.connector.Error as err:
            # Rollback the transaction on error
            self.connection.rollback()
            print(f"Error: {err}")
        finally:
            cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()

# Usage example:
if __name__ == "__main__":
    # Initialize the DocumentPersister with your database credentials
    persister = DocumentPersister(host="your_host", user="your_user", password="your_password", database="your_database")

    # Create a Document instance (replace with your data)
    document = Document(document_id=None, doc_type="PDF", text="Sample document")

    # Add Metadata and Chunk instances to the Document (replace with your data)
    metadata1 = Metadata(metadata_id=None, document_id=None, key="Author", value="John Doe")
    chunk1 = Chunk(chunk_id=None, document_id=None, content="Chunk 1 content")

    document.metadata.append(metadata1)
    document.chunks.append(chunk1)

    try:
        # Persist the Document and associated objects
        persister.persist_document(document)
        print("Document persisted successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        persister.close()
