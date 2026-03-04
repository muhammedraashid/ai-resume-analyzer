from fastapi import APIRouter, File, HTTPException, UploadFile
import shutil
import os
import re
from uuid import uuid4

from app.services.resume_parser import extract_resume_text
from app.core.logger import logger

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

def clean_filename(filename: str) -> str:
    filename = re.sub(r"[^\w\-. ]", "", filename)
    filename = filename.replace(" ", "_")
    return filename


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
      
        extension = os.path.splitext(file.filename)[1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX formats are allowed"
            )

        clean_name = clean_filename(file.filename)
        unique_name = f"{uuid4().hex}_{clean_name}"

        file_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resume_text = extract_resume_text(file_path)

        return {
            "fileSavedAs":unique_name,
            "textPreview": resume_text[:1000]
        }
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Upload failed: {e}")

        raise HTTPException(
            status_code=500,
            detail="Resume upload failed"
        )