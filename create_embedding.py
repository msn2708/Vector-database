from sentence_transformers import SentenceTransformer
import numpy as np
from get_config import Config
import torch as torch

#this needs to be exposed as a gRPC service. 
config = Config().get_config()
MODEL = SentenceTransformer(config['models']['embedding_model'])

def get_embedding(text):
    if torch.cuda.is_available():
        device = torch.device('cuda')
        MODEL.to('cuda')
    return MODEL.encode(text).tobytes()