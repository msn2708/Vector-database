from sentence_transformers import SentenceTransformer
import numpy as np
from get_config import Config
import torch as torch

#this needs to be exposed as a gRPC service. 
config = Config().get_config()
MODEL = SentenceTransformer(config['models']['embedding_model'])
device = "cuda:0" if torch.cuda.is_available() else "cpu"

def get_embedding(text):
    MODEL.to(device)
    return MODEL.encode(text).tobytes()

#print(str(get_embedding("This is a sentence")))