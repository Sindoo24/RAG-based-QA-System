import requests
from config import QWEN_API_URL, QWEN_MODEL

def flatten_output(item):
    """
    Recursively flatten an output item to extract all string content.
    """
    if isinstance(item, str):
        return [item]
    elif isinstance(item, list):
        result = []
        for x in item:
            result.extend(flatten_output(x))
        return result
    elif isinstance(item, dict):
        texts = []
        for key in ["text", "content"]:
            if key in item:
                texts.extend(flatten_output(item[key]))
        return texts
    else:
        return []

def generate_answer(query, retrieved_chunks):
    # Build context
    context_text = "\n\n".join([f"[Page {c['metadata']['page']}] {c['content']}" for c in retrieved_chunks])
    prompt = f"Answer the following question based on the context below. Include citations from pages.\n\nContext:\n{context_text}\n\nQuestion: {query}\nAnswer:"

    payload = {
        "model": QWEN_MODEL,
        "input": prompt,   
        "temperature": 0,
        "max_output_tokens": 500
    }

    response = requests.post(QWEN_API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        

        if "output" in data and isinstance(data["output"], list):
            answer_texts = []
            for item in data["output"]:
                answer_texts.extend(flatten_output(item))
            return "\n".join(answer_texts) if answer_texts else "No answer returned."
        else:
            return "No output returned from API."
    else:
        return f"Error: {response.status_code} - {response.text}"

