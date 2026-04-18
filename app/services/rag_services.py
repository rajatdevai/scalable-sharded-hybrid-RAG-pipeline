from app.utils.embedding import embed_batch
from app.utils.cache import get_cache, set_cache
from app.utils.reranker import rerank
from app.services.retriever import hybrid_retrieve
from app.utils.llm import generate_response
from app.config.settings import FINAL_K

def rag_pipeline(query):

    # 1. Check cache
    cached = get_cache(query)
    if cached:
        return cached

    # 2. Embed query
    query_vec = embed_batch([query])[0]

    # 3. Retrieve
    shards = ["hr_leave", "hr_salary", "hr_general"]
    docs = hybrid_retrieve(query, shards, query_vec, docs_per_shard=10)

    # 4. Re-rank
    reranked = rerank(query, docs)

    # 5. Generate final answer
    prompt = f"""Context: {reranked}
    Question: {query}
    Answer:"""

    final_answer = generate_response(prompt)

    # 6. Cache and return
    set_cache(query, final_answer)
    return final_answer