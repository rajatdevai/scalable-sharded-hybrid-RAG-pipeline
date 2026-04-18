import os
import pickle
from rank_bm25 import BM25Okapi
from app.config.settings import FAISS_PATH

bm25_store = {}

def get_bm25_path(shard_name):
    return os.path.join(FAISS_PATH, f"{shard_name}_bm25.pkl")

def build_bm25(shard_name, docs):
    # Ensure directory exists
    os.makedirs(FAISS_PATH, exist_ok=True)
    
    # Docs are list of strings or dicts with 'text'
    texts = [d['text'] if isinstance(d, dict) else d for d in docs]
    tokenized_docs = [doc.split() for doc in texts]
    
    bm25 = BM25Okapi(tokenized_docs)
    bm25_store[shard_name] = bm25
    
    # Save to disk
    path = get_bm25_path(shard_name)
    with open(path, "wb") as f:
        pickle.dump(bm25, f)

def search_bm25(shard_name, query, docs, k=10):
    bm25 = bm25_store.get(shard_name)

    if not bm25:
        # Try loading from disk
        path = get_bm25_path(shard_name)
        if os.path.exists(path):
            with open(path, "rb") as f:
                bm25 = pickle.load(f)
                bm25_store[shard_name] = bm25
        else:
            return []

    scores = bm25.get_scores(query.split())
    # Ensure docs matches indices in BM25
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    return [docs[i] for i in top_idx if i < len(docs)]

