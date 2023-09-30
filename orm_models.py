from sqlmodel import SQLModel, Field, Relationship
from get_config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from typing import Optional
from create_embedding import get_embedding
from get_paragraphs import get_paragraphs
from paragraph_segmentation import ParagraphSegmenter


config = Config().get_config()
engine = create_engine(config.get('db_url'),echo=True)
    
class Document(SQLModel, table=True):
    document_id: int  = Field(default=None, primary_key=True)
    doc_type: str
    file_name: str
    text: str
    # chunks: list["Chunk"] = Relationship(back_populates="document", sa_relationship_kwargs={"primaryjoin": "Chunk.document_id==Document.document_id", "lazy": "joined",})
    chunks: list["Chunk"] = Relationship(back_populates="document")
    dict_metadata: list["Metadata"] = Relationship(back_populates="document")
    
    def create_chunks(self):
        #paragraphs = get_paragraphs(self.text)
        paragraphs = ParagraphSegmenter().create_paragraph(self.text)
        for paragraph in paragraphs:
            embedding = get_embedding(paragraph) #create a vector embedding here
            if embedding is None:
                continue
            
            chunk = Chunk(document=self, text=paragraph, embedding=embedding)
            self.chunks.append(chunk)            
        
    def create_metadata(self, metadata:dict):
        for key in metadata:
            self.dict_metadata.append(Metadata(
                key=key, 
                value=metadata[key],
                document=self))
            
class Chunk(SQLModel, table=True):
    chunk_id: int = Field(default=None, primary_key=True)
    text: str
    embedding: bytes

    document_id: Optional[int] = Field(default=None, foreign_key="document.document_id")
    document: Optional[Document] = Relationship(back_populates="chunks")
    
    def save (self, *args, **kwargs):
        super(Chunk, self).save(*args, **kwargs)
        
class Metadata(SQLModel, table=True):
    metadata_id: Optional[int] = Field(default=None, primary_key=True)
    key: str
    value: str
    
    document_id: int = Field(default=None, foreign_key="document.document_id")
    document: Document = Relationship(back_populates="dict_metadata")
    
SQLModel.metadata.reflect(engine)

