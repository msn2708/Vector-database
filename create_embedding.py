from sentence_transformers import SentenceTransformer
import numpy as np
from get_config import Config
import json

MODEL = SentenceTransformer(Config().get_config().get('embedding_model'))

def get_embedding(text):
    embeddings = MODEL.encode(text)
    return [json.dumps(embeddings.tolist()) for embedding in embeddings]

    #return MODEL.encode(text).flatten()