from app.utils.vector_store import search , load_or_create_index
from app.utils.bm25 import search_bm25


def hybrid_retrieve(query, shards, query_vec,docs_per_shard=10):

    all_results = []

    for shard in shards:
        load_or_create_index(shard)

        # BM25 first (fast)
        bm25_docs = search_bm25(shard, query, documents[shard], docs_per_shard)

        # Then dense
        dense_docs = search(shard, query_vec, docs_per_shard)

        # Combine
        combined = list(set(bm25_docs + dense_docs))
        all_results.extend(combined)

        #remove dupliacte
        seen= set()
        unique_results=[]
        for doc in all_results:
            if doc not in seen:
                unique_results.append(doc)
                seen.add(doc)
        all_results=unique_results

    # Re-rank
    reranked = rerank(query, all_results)

    return reranked[:FINAL_K]


def rerank(query, docs):

    prompt = f"""Context: {docs}
    Question: {query}
    Rank the documents by relevance (1 = most relevant). Return only the documents in order."""

    return generate_response(prompt)