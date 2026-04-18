import os
FAISS_PATH="vectorstores/faiss_indexes"
REDIS_URL="redis://localhost:6379/0"
EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
# RERANKER_MODEL="BAAI/bge-reranker-base"
RERANKER_MODEL="cross-encoder/ms-marco-MiniLM-L-6-v2"
TOP_K=10
FINAL_K=3
CHUNK_SIZE=500
CHUNK_OVERLAP=50