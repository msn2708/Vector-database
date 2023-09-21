import yaml
import sentence_transformers
import spacy
from get_config import get_config

def create_paragraph(content):
    config = get_config()

    # Use Spacy to return an array of sentences from this corpus
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(content)
    #Set p=s1. Now compare p and s2. If they are similar, p=p+s2. Continue until p#s(n)
    for sent in doc.sents:
        print(sent.text) 
    
#create a main program to invoke
if __name__ == "__main__":
    create_paragraph("This is ia sentence. And this is another one. The end")

