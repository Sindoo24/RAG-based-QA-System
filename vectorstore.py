import chromadb
from chromadb.config import Settings
from config import CHROMA_DB_PATH

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection("multimodal_docs")

def add_chunks_to_vectorstore(chunks):
    for c in chunks:
        collection.add(
            ids=[c['id']],
            embeddings=[c['embedding']],
            documents=[c['content']],
            metadatas=[c['metadata']]
        )

def query_vectorstore(query_embedding, top_k=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    chunks = []
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        chunks.append({"content": doc, "metadata": meta})
    return chunks
