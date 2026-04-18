from rank_bm25 import BM25Okapi
bm25_store={}

def build_bm25(shard_name,docs):
    tokenized_docs=[doc.split() for doc in docs]
    bm25_store[shard_name]=BM25Okapi(tokenized_docs)

def search_bm25(shard_name, query, docs, k=10):

    bm25 = bm25_store.get(shard_name)

    if not bm25:
        return []

    scores = bm25.get_scores(query.split())
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    return [docs[i] for i in top_idx]
