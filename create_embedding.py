from sentence_transformers import SentenceTransformer
import numpy as np
from get_config import Config

#this needs to be exposed as a gRPC service. 
config = Config().get_config()
MODEL = SentenceTransformer(config['models']['embedding_model'])

def get_embedding(text):   
    return MODEL.encode(text).tobytes()