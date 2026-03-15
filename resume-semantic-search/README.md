# Semantic Resume Search using Endee Vector Database

## Project Overview

This project implements a **Semantic Resume Search Engine** using the **Endee Vector Database**.

Traditional resume filtering systems rely on keyword matching, which fails when different words express similar concepts. For example, a job description asking for *“Python backend engineer”* may fail to match a resume that describes *“Django developer”* even though both represent the same skill set.

This system solves that problem by converting resumes and job descriptions into **vector embeddings** and performing **semantic similarity search** using Endee.

The result is a system that retrieves the most contextually relevant resumes for a given job description.

---

## Problem Statement

Recruiters often need to review hundreds of resumes to find suitable candidates for a job role. Keyword-based filtering is unreliable because it does not capture semantic meaning.

Example:

Job Description

```
Looking for a React developer with machine learning experience.
```

Resume Text

```
Developed frontend interfaces using Next.js and trained neural network models for recommendation systems.
```

Keyword matching may fail here, but **semantic embeddings recognize the similarity between these concepts.**

This project demonstrates how **vector search can improve candidate matching**.

---

## System Architecture

```
PDF Resume Upload
        ↓
Text Extraction (pdfplumber)
        ↓
Embedding Generation (Sentence Transformers)
        ↓
Endee Vector Database
        ↓
Semantic Similarity Search
        ↓
Top Matching Candidate Resumes
```

---

## Technology Stack

**Embedding Model**

* Sentence Transformers
* Model: `all-MiniLM-L6-v2`

**Vector Database**

* Endee Vector Database
* Stores resume embeddings and performs similarity search

**Backend**

* FastAPI
* Uvicorn server

**Data Processing**

* pdfplumber for extracting text from resumes

**Frontend**

* HTML
* CSS
* JavaScript (Fetch API)

---

## How Endee is Used

Endee serves as the **vector storage and retrieval engine** for the application.

Workflow:

1. Resume text is extracted from uploaded PDFs.
2. The text is converted into a **384-dimensional embedding** using the Sentence Transformers model.
3. The embedding is stored in the **Endee vector database** along with metadata containing the original resume text.
4. When a user enters a job description, the system generates an embedding for the query.
5. Endee performs **cosine similarity search** to find the most relevant resumes.
6. The top results are returned with similarity scores.

---

## Project Workflow

### Resume Upload

1. User uploads a PDF resume.
2. Backend extracts text using `pdfplumber`.
3. The text is converted into an embedding.
4. The embedding and metadata are stored in Endee.

### Semantic Search

1. User enters a job description.
2. The description is converted into an embedding.
3. Endee searches the vector database.
4. The system returns the most similar resumes ranked by similarity score.

---

## Example Query

Query:

```
Looking for a Python machine learning engineer with frontend experience
```

Example Results:

```
1. John Doe — Similarity Score: 0.92
2. Alice Smith — Similarity Score: 0.88
3. David Brown — Similarity Score: 0.84
```

---

## Setup Instructions

### Clone the Repository

```
git clone https://github.com/vedansha07/endee.git
cd endee/resume-semantic-search
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Run the Server

```
uvicorn backend.main:app --reload
```

API documentation will be available at:

```
http://127.0.0.1:8000/docs
```

---

## Limitations

Currently the vector database runs during the FastAPI session.
If the server restarts, resumes must be re-uploaded.

In a production environment, the Endee database would be configured with persistent storage to retain embeddings across restarts.

---

## Future Improvements

* Resume skill extraction using NLP
* Hybrid search (keyword + vector search)
* Candidate recommendation system
* Retrieval-Augmented Generation (RAG) for automatic candidate summaries
