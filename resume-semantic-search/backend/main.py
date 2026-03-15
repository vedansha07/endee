from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from embedder import generate_embedding
from vector_store import store_resume, search_resumes

app = FastAPI()

class UploadRequest(BaseModel):
    resume_id: str
    text: str

class SearchRequest(BaseModel):
    job_description: str

@app.post("/upload")
def upload_resume(request: UploadRequest):
    embedding = generate_embedding(request.text)
    store_resume(request.resume_id, request.text, embedding)
    return {"message": "Resume stored successfully"}

@app.post("/search")
def search_resumes_endpoint(request: SearchRequest):
    query_embedding = generate_embedding(request.job_description)
    results = search_resumes(query_embedding)
    return results
