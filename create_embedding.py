from sentence_transformers import SentenceTransformer
import numpy as np
from get_config import Config

MODEL = SentenceTransformer(Config().get_config().get('embedding_model'))

def get_embedding(text):
    return MODEL.encode(text)