# from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship

# Base = declarative_base()

# class Document(Base):
#     __tablename__ = "document"

#     id = Column(Integer, primary_key=True)
#     doc_type = Column(String)
#     text = Column(Text)
#     file_name = Column(Text)
#     chunks = relationship("Chunk", back_populates="document")
#     dict_metadata: relationship("Metadata",back_populates="document")
    
#     def create_chunks(self):
#         paragraphs = self.text.split("\n\n")
        
#         for paragraph in paragraphs:
#             embedding = '' #create a vector embedding here
#             chunk = Chunk(document=self, text=paragraph, embedding=embedding)
#             self.chunks.append(chunk)            
        
#     def create_metadata(self, metadata:dict):
#         for key, value in metadata:
#             self.dict_metadata.append(Metadata(
#                 key=key, 
#                 value=value,
#                 document=self))
            
# class Chunk(Base):
#     __tablename__ = "chunk"
    
#     id = Column(Integer, primary_key=True)
#     text = Column(Text)
#     embedding = Column(Text)
    
#     document_id = Column(Integer, ForeignKey("document.id"))
#     document = relationship("Document", back_populates="chunks")
    
# class Metadata(Base):
#     __tablename__ = "metadata"

#     id = Column(Integer, primary_key=True)
#     key = Column(String)
#     value = Column(String)
    
#     document_id = Column(Integer, ForeignKey("document.id"))
    
from sqlmodel import SQLModel, Field, Relationship
import os
from get_config import get_config
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from typing import Optional


engine = create_engine(get_config().get('db_url'),echo=True)

class Document(SQLModel, table=True):
    #__table_args__ = {'extend_existing': True}
    __tablename__ = "vectordb.document"
    
    document_id: int  = Field(default=None, primary_key=True)
    doc_type: str
    file_name: str
    text: str
    chunks: list["Chunk"] = Relationship(back_populates="document")
    dict_metadata: list["Metadata"] = Relationship(back_populates="document")
    
    class Config:
        tablename = "document"
    
    def create_chunks(self):
        paragraphs = self.text.split("\n\n")
        
        for paragraph in paragraphs:
            embedding = '' #create a vector embedding here
            chunk = Chunk(document=self, text=paragraph, embedding=embedding)
            self.chunks.append(chunk)            
        
    def create_metadata(self, metadata:dict):
        for key, value in metadata:
            self.dict_metadata.append(Metadata(
                key=key, 
                value=value,
                document=self))
            
            

class Chunk(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "chunk"
    chunk_id: int = Field(default=None, primary_key=True)
    text: str
    embedding: str

    document_id: int = Field(foreign_key="document.document_id")
    document: Document = Relationship(back_populates="chunks")

class Metadata(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "metadata"
    metadata_id: Optional[int] = Field(default=None, primary_key=True)
    key: str
    value: str
    
    document_id: int = Field(foreign_key="document.document_id")
    document: Document = Relationship(back_populates="dict_metadata")
    
SQLModel.metadata.reflect(engine)

