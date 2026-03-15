import pdfplumber

def extract_text(file_path: str) -> str:
    extracted_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
    return "\n".join(extracted_text)
