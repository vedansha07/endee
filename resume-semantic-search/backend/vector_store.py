from endee import Endee

client = Endee()

def get_collection():
    try:
        return client.create_index("resumes", dimension=384, space_type="cosine")
    except Exception:
        return client.get_index("resumes")

def store_resume(resume_id: str, text: str, embedding: list):
    collection = get_collection()
    collection.upsert([
        {
            "id": resume_id,
            "vector": list(embedding),
            "meta": {"text": text}
        }
    ])

def search_resumes(query_embedding: list):
    collection = get_collection()
    response = collection.query(
        vector=list(query_embedding),
        top_k=5
    )
    results = []
    for res in response:
        results.append({
            "id": res["id"],
            "score": res["similarity"],
            "metadata": res.get("meta", {})
        })
    return results

def clear_db():
    try:
        client.delete_index("resumes")
    except Exception as e:
        print(f"Error clearing db: {e}")
        pass
