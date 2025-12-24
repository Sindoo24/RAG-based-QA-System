from sentence_transformers import SentenceTransformer

# Load text embedding model
text_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_text_embedding(text):
    """Return embedding vector for a given text string."""
    return text_model.encode(text)

def chunk_document(doc_data):
    """
    Convert document data into chunks with embeddings and metadata.
    Handles text, tables, and OCR text from images.
    """
    chunks = []
    chunk_id = 0

    # ---------------- Text chunks ----------------
    for t in doc_data.get("text", []):
        paragraphs = t["text"].split("\n\n")
        for p in paragraphs:
            if p.strip():
                chunks.append({
                    "id": f"chunk_{chunk_id}",
                    "content": p.strip(),
                    "embedding": get_text_embedding(p.strip()),
                    "metadata": {"page": t["page"], "type": "text"}
                })
                chunk_id += 1

    # ---------------- Table chunks ----------------
    for t in doc_data.get("tables", []):
        table_str = t["table"].to_string()
        chunks.append({
            "id": f"chunk_{chunk_id}",
            "content": table_str,
            "embedding": get_text_embedding(table_str),
            "metadata": {"page": t["page"], "type": "table"}
        })
        chunk_id += 1

    # ---------------- Image OCR chunks ----------------
    for img in doc_data.get("images", []):
        if img["ocr_text"].strip():
            chunks.append({
                "id": f"chunk_{chunk_id}",
                "content": img["ocr_text"],
                "embedding": get_text_embedding(img["ocr_text"]),
                "metadata": {"page": img["page"], "type": "image"}
            })
            chunk_id += 1

    return chunks
