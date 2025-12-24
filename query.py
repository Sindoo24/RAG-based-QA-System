from chunking_embedding import get_text_embedding
from vectorstore import query_vectorstore

def retrieve_relevant_chunks(query, top_k=5):
    query_emb = get_text_embedding(query)
    chunks = query_vectorstore(query_emb, top_k=top_k)
    return chunks
