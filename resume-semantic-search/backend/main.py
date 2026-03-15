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

from typing import Optional

@app.post("/search")
async def search_resumes_endpoint(
    job_description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    if not job_description and not file:
        raise HTTPException(status_code=400, detail="Must provide either text job description or upload a PDF")
    
    text = job_description
    if file:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File must be a PDF")
        text = extract_text_from_pdf(file.file)
        
    query_embedding = generate_embedding(text)
    results = search_resumes(query_embedding)
    return results
