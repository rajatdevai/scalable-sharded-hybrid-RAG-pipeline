from app.utils.vector_store import search, load_or_create_index, documents, get_available_shards
from app.utils.bm25 import search_bm25
from app.utils.reranker import rerank
from app.utils.router import classify_text
from app.config.settings import FINAL_K
from app.config.constants import ALLOWED_CATEGORIES

def select_relevant_shards(query):
    """
    Uses AI to identify which categories are relevant to the user's query.
    """
    # Use multi-label classification to catch queries that span multiple topics
    relevant_categories = classify_text(query, ALLOWED_CATEGORIES, multi_label=True)
    
    # Map to shard names
    relevant_shards = [f"{cat.lower()}_shard" for cat in relevant_categories]
    
    # Always check if these shards actually exist on disk
    available_shards = get_available_shards()
    
    final_shards = [s for s in relevant_shards if s in available_shards]
    
    # Fallback to general_shard or all available if none found
    if not final_shards:
        if "general_shard" in available_shards:
            return ["general_shard"]
        return available_shards
        
    return final_shards

def hybrid_retrieve(query, query_vec, docs_per_shard=10):
    all_results = []
    
    # Identify relevant shards dynamically
    shards = select_relevant_shards(query)

    for shard in shards:
        load_or_create_index(shard)

        # 1. BM25 search (ensure docs list is available)
        shard_docs = documents.get(shard, [])
        if not shard_docs:
            continue
            
        bm25_docs = search_bm25(shard, query, shard_docs, docs_per_shard)

        # 2. Dense search
        dense_docs = search(shard, query_vec, docs_per_shard)

        # 3. Combine results for this shard
        combined = list(set(bm25_docs + dense_docs))
        all_results.extend(combined)

    # 4. Global de-duplication
    seen = set()
    unique_results = []
    for doc in all_results:
        if doc not in seen:
            unique_results.append(doc)
            seen.add(doc)
    
    if not unique_results:
        return []

    # 5. Re-rank the combined results
    reranked = rerank(query, unique_results)

    # 6. Return top K
    return reranked[:FINAL_K]
