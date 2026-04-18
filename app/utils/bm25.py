from rank_bm25 import BM25Okapi
bm25_store={}

def build_bm25(shard_name,docs):
    tokenized_docs=[doc.split() for doc in docs]
    bm25_store[shard_name]=BM25Okapi(tokenized_docs)

def search_bm25(shard_name,query,k=10):
    tokenized_query=query.split()
    bm25=bm25_store[shard_name]
    return bm25.get_top_n(tokenized_query,chunks,n=k)

