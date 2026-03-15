import pdfplumber
from typing import IO

def extract_text_from_pdf(file: IO) -> str:
    extracted_text = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
    return "\n".join(extracted_text)
