from endee import Client

client = Client()

try:
    collection = client.create_collection("resumes")
except Exception:
    collection = client.get_collection("resumes")

def store_resume(resume_id: str, text: str, embedding: list):
    collection.add(
        id=resume_id,
        vector=embedding,
        metadata={"text": text}
    )

def search_resumes(query_embedding: list):
    results = collection.search(
        vector=query_embedding,
        top_k=5
    )
    return results
