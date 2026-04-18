import faiss
import numpy as np
import os
from app.config.settings import FAISS_PATH

dimension = 384

indexes = {}
documents = {}

def load_or_create_index(shard_name):

    path = os.path.join(FAISS_PATH, f"{shard_name}.index")

    if os.path.exists(path):
        index = faiss.read_index(path)
    else:
        index = faiss.IndexFlatL2(dimension)

    indexes[shard_name] = index
    documents[shard_name] = []

def add_documents(shard_name, vectors, docs):

    index = indexes[shard_name]
    index.add(np.array(vectors).astype("float32"))
    documents[shard_name].extend(docs)

def search(shard_name, query_vec, k=10):

    index = indexes[shard_name]
    D, I = index.search(np.array([query_vec]).astype("float32"), k)

    return [documents[shard_name][i] for i in I[0] if i < len(documents[shard_name])]