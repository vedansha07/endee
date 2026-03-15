try:
    from endee import Client
except ImportError:
    # A lightweight in-memory mock to let the FastAPI server run if the endee python package is not available
    import numpy as np
    class Client:
        def __init__(self):
            self._collections = {}
        def create_collection(self, name):
            if name not in self._collections:
                self._collections[name] = self.Collection(name)
            return self._collections[name]
        def get_collection(self, name):
            return self._collections[name]

        class Collection:
            def __init__(self, name):
                self.name = name
                self.data = []
            def add(self, id, vector, metadata):
                self.data.append({"id": id, "vector": vector, "metadata": metadata})
            def search(self, vector, top_k):
                if not self.data: return []
                vectors = np.array([item["vector"] for item in self.data])
                query = np.array(vector)
                norms = np.linalg.norm(vectors, axis=1) * np.linalg.norm(query)
                scores = np.dot(vectors, query) / np.maximum(norms, 1e-9)
                results = []
                for i, idx in enumerate(np.argsort(scores)[::-1]):
                    if i >= top_k: break
                    results.append({"id": self.data[idx]["id"], "score": float(scores[idx]), "metadata": self.data[idx]["metadata"]})
                return results

client = Client()
try:
    collection = client.create_collection("resumes")
except Exception:
    collection = client.get_collection("resumes")

def store_resume(resume_id, text, embedding):
    collection.add(
        id=resume_id,
        vector=embedding,
        metadata={"text": text}
    )

def search_resumes(query_embedding):
    results = collection.search(
        vector=query_embedding,
        top_k=5
    )
    return results
