class Document:
    def __init__(self, document_id, file_name, doc_type, text):
        self.document_id = document_id
        self.doc_type = doc_type
        self.text = text
        self.file_name = file_name
        self.chunks = []  # Initialize as an empty list to hold Chunk objects
        self.metadata = []  # Initialize as an empty list to hold Metadata objects

    def add_chunk(self, chunk):
        if isinstance(chunk, Chunk):
            self.chunks.append(chunk)
        else:
            raise ValueError("Invalid chunk object")

    def add_metadata(self, metadata):
        if isinstance(metadata, Metadata):
            self.metadata.append(metadata)
        else:
            raise ValueError("Invalid metadata object")

class Chunk:
    def __init__(self, chunk_id, document_id, content):
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.content = content

class Metadata:
    def __init__(self, metadata_id, document_id, key, value):
        self.metadata_id = metadata_id
        self.document_id = document_id
        self.key = key
        self.value = value
            
