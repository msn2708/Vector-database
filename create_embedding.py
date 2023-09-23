from sentence_transformers import SentenceTransformer
import numpy as np
from get_config import Config
import json

MODEL = SentenceTransformer(Config().get_config().get('embedding_model'))

def get_embedding(text):
    return MODEL.encode(text).tobytes()
    #print(embeddings.tobytes())   
    #return ''.join([json.dumps(embedding.tolist()) for embedding in embeddings])

#get_embedding("This is a sentence")