
import re

from docx import Document
import os
import pdfplumber

from app.core.exceptions import ResumeParsingException, UnsupportedFileException
from app.core.logger import logger

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text_from_pdf(file_path:str)->str:
    text = ""
    try:

        with pdfplumber.open() as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return clean_text(text=text)
    except Exception as e :
        logger.error(f"PDF parsing failed:{e}")
        return ResumeParsingException()

def extract_text_from_docx(file_path:str)->str:
    try:
        doc = Document(file_path)
        text = "\n".join([par.text for par in doc.paragraphs])
        return clean_text(text=text)
    except Exception as e :
        logger.error(f"DOCX parsing failed: {e}")
        return ResumeParsingException()


def extract_resume_text(file_path:str)->str:
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension == ".pdf":
        return extract_text_from_pdf(file_path=file_path)
    elif extension == ".docx":
        return extract_text_from_docx(file_path=file_path)
    
    else:
        raise UnsupportedFileException()