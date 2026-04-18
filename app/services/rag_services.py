from app.utils.embedding import embed_batch
from app.utils.cache import get_cache, set_cache
from app.services.retriever import hybrid_retrieve
from app.utils.llm import generate_response

def rag_pipeline(query):

    # 1. Check cache
    cached = get_cache(query)
    if cached:
        return cached

    # 2. Embed query
    query_vec = embed_batch([query])[0]

    # 3. Retrieve & Re-rank
    # Note: hybrid_retrieve now handles dynamic shard selection using AI
    context_docs = hybrid_retrieve(query, query_vec, docs_per_shard=10)

    # 4. Generate final answer
    if not context_docs:
        context_str = "No relevant documents found."
    else:
        context_str = "\n".join(context_docs)


    prompt = f"""Use the following pieces of context to answer the question at the end. 
Keep the answer concise and professional.

Context:
{context_str}

Question: {query}
Answer:"""

    final_answer = generate_response(prompt)

    # 5. Cache and return
    set_cache(query, final_answer)
    return final_answer