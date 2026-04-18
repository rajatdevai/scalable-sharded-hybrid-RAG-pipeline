from sentence_transformers import SentenceTransformer
from app.config.settings import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def embed(text):
    return model.encode(text)
def embed_batch(texts):
    return model.encode(texts)
    