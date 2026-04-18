from app.utils.embedding import embed_batch
from app.utils.vector_store import add_documents, load_or_create_index
from app.utils.bm25 import build_bm25
from app.services.shard_manager import get_shard
from app.utils.chunking import recursive_character_splitter

def ingest_documents(docs):
    # docs is a list of strings
    for doc in docs:
        shard = get_shard(doc)
        load_or_create_index(shard)

        # 1. Chunking
        chunks = recursive_character_splitter(doc)
        
        # 2. Embedding
        vectors = embed_batch(chunks)

        # 3. Add to Vector Store (persists automatically)
        add_documents(shard, vectors, chunks)

        # 4. Build BM25 Index (persists automatically)
        # Note: In a real persistent system, we should load existing BM25, 
        # add new documents, and rebuild. For simplicity, we get all docs and rebuild.
        from app.utils.vector_store import documents
        if shard in documents:
            build_bm25(shard, documents[shard])