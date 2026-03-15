import pdfplumber
import io

def extract_text_from_pdf(file_bytes) -> str:
    """
    Extract text from a PDF file object.
    Tries pdfplumber first; falls back to PyMuPDF (fitz) for image-based or complex PDFs.
    """
    # Read bytes once into memory (supports both file-like objects and raw bytes)
    if hasattr(file_bytes, 'read'):
        data = file_bytes.read()
    else:
        data = file_bytes

    # Attempt 1: pdfplumber (handles standard text-layer PDFs well)
    try:
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
        if text:
            return text
    except Exception:
        pass

    # Attempt 2: PyMuPDF (fitz) – handles more complex PDF structures
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=data, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc).strip()
        doc.close()
        if text:
            return text
    except Exception:
        pass

    return ""
