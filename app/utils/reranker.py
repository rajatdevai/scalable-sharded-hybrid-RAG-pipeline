from sentence_transformers import CrossEncoder
from app.config.settings import RERANKER_MODEL

model = CrossEncoder(RERANKER_MODEL)

def rerank(query, docs):

    pairs = [[query, doc] for doc in docs]
    scores = model.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in ranked]