# Semantic Resume Search using Endee Vector Database

## Problem Statement

Recruiters manually review hundreds of resumes. Keyword-based search fails because it cannot understand semantic meaning.

**Example**:
- **Job description**: "React developer with ML experience"
- **Resume text**: "Built frontend apps using Next.js and trained neural networks."

Keyword search fails, but semantic search succeeds because it understands the intrinsic meaning.

## Solution

This project builds a semantic search system that converts resumes into vector embeddings and stores them inside the Endee vector database. 

Recruiter queries are embedded and compared against stored resume embeddings to retrieve the most relevant candidates quickly and accurately.

## System Architecture

**Resume → Embedding → Endee Vector DB → Semantic Search → Ranked Results**

1. Uploaded resumes are textually parsed to extract meaningful data.
2. The parsed text is embedded mathematically using a dense embedding model (`sentence-transformers`).
3. These vector embeddings are stored inside the `Endee Vector Database` mapped to text metadata.
4. User queries are similarly embedded and retrieved via semantic similarity search.

## Tech Stack

- **Python**
- **FastAPI**
- **Sentence Transformers**
- **Endee Vector Database**
- **pdfplumber**

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/vedansha07/endee.git
cd endee/resume-semantic-search
```

### 2. Create a Virtual Environment and Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### 3. Run the API Server
```bash
cd backend
uvicorn main:app --reload
```
The server will run at `http://127.0.0.1:8000`. You can access the Swagger documentation at `http://127.0.0.1:8000/docs`.

## Example Query

Once the application is running, you can ingest resumes via the `POST /upload` endpoint and search using `POST /search`.

**Upload Example:**
```json
{
  "resume_id": "resume1",
  "text": "John Doe. Skills: Python, Machine Learning, React, FastAPI."
}
```

**Search Example:**
```json
{
  "job_description": "Looking for Python machine learning engineer with frontend experience"
}
```

**Search Result:**
The system returns resumes ranked by semantic similarity based on their vector embeddings from the Endee vector database.
