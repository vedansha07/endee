from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
import sys
import os

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from embedder import generate_embedding
from vector_store import store_resume, search_resumes
from resume_parser import extract_text_from_pdf

app = FastAPI(title="Semantic Resume Search", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve the frontend directory relative to project root (resume-semantic-search/)
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
FRONTEND_DIR = os.path.normpath(FRONTEND_DIR)

# Serve /static/* from the frontend folder
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def serve_frontend():
    """Serve the main HTML UI."""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.post("/upload")
async def upload_resume(resume_id: str = Form(...), file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    text = extract_text_from_pdf(file.file)

    if not text or not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from PDF. Ensure the PDF contains selectable text.")

    embedding = generate_embedding(text)

    try:
        store_resume(resume_id, text, embedding)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=503, detail="Vector Database is unavailable. Please ensure the Endee DB server is running.")

    return {"message": "Resume successfully stored and embedded in Endee"}


@app.post("/search")
async def search_resumes_endpoint(
    job_description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    if not job_description and not file:
        raise HTTPException(status_code=400, detail="Must provide either a text job description or upload a PDF.")

    text = job_description
    if file:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        text = extract_text_from_pdf(file.file)
        if not text or not text.strip():
            raise HTTPException(status_code=422, detail="Could not extract text from PDF.")

    query_embedding = generate_embedding(text)

    try:
        results = search_resumes(query_embedding)
    except Exception as e:
        raise HTTPException(status_code=503, detail="Vector Database is unavailable. Please ensure the Endee DB server is running.")

    return results


@app.delete("/clear")
async def clear_database():
    try:
        from vector_store import clear_db
        clear_db()
        return {"message": "Database cleared successfully"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to clear database")
