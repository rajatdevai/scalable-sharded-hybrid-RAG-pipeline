import faiss
import numpy as np
import os
import json
from app.config.settings import FAISS_PATH

dimension = 384

indexes = {}
documents = {}

def get_metadata_path(shard_name):
    return os.path.join(FAISS_PATH, f"{shard_name}_metadata.json")

def load_or_create_index(shard_name):
    # Ensure directory exists
    os.makedirs(FAISS_PATH, exist_ok=True)
    
    path = os.path.join(FAISS_PATH, f"{shard_name}.index")
    meta_path = get_metadata_path(shard_name)

    if os.path.exists(path):
        index = faiss.read_index(path)
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                documents[shard_name] = json.load(f)
        else:
            documents[shard_name] = []
    else:
        index = faiss.IndexFlatL2(dimension)
        documents[shard_name] = []

    indexes[shard_name] = index

def add_documents(shard_name, vectors, docs):
    if shard_name not in indexes:
        load_or_create_index(shard_name)
        
    index = indexes[shard_name]
    index.add(np.array(vectors).astype("float32"))
    
    # Update documents list
    documents[shard_name].extend(docs)
    
    # Save index and metadata
    path = os.path.join(FAISS_PATH, f"{shard_name}.index")
    meta_path = get_metadata_path(shard_name)
    
    faiss.write_index(index, path)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(documents[shard_name], f, ensure_ascii=False, indent=2)

def get_available_shards():
    """
    Returns a list of all shards that currently have a FAISS index on disk.
    """
    if not os.path.exists(FAISS_PATH):
        return []
        
    shards = []
    for f in os.listdir(FAISS_PATH):
        if f.endswith(".index"):
            shards.append(f.replace(".index", ""))
    return shards

def search(shard_name, query_vec, k=10):

    if shard_name not in indexes:
        load_or_create_index(shard_name)
        
    index = indexes[shard_name]
    
    if index.ntotal == 0:
        return []
        
    D, I = index.search(np.array([query_vec]).astype("float32"), k)

    results = []
    for i in I[0]:
        if i != -1 and i < len(documents[shard_name]):
            results.append(documents[shard_name][i])
    return results