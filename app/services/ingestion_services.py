from app.utils.embedding import embed_batch
from app.utils.vector_store import add_documents, load_or_create_index
from app.utils.bm25 import build_bm25
from app.services.shard_manager import get_shard

def ingest_documents(docs):

    for doc in docs:

        shard = get_shard(doc)

        load_or_create_index(shard)

        chunks = [{"text": doc}]

        vectors = embed_batch([doc])

        add_documents(shard, vectors, chunks)

        build_bm25(shard, chunks)