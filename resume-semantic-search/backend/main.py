from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from embedder import generate_embedding
from vector_store import store_resume, search_resumes
from resume_parser import extract_text_from_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    job_description: str

@app.post("/upload")
async def upload_resume(resume_id: str = Form(...), file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    text = extract_text_from_pdf(file.file)
    embedding = generate_embedding(text)
    store_resume(resume_id, text, embedding)
    
    return {"message": "Resume successfully stored and embedded in Endee"}

@app.post("/search")
def search_resumes_endpoint(request: SearchRequest):
    query_embedding = generate_embedding(request.job_description)
    results = search_resumes(query_embedding)
    return results
