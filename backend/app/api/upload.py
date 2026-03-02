from fastapi import APIRouter, UploadFile, File
import shutil
import os
import re
from uuid import uuid4

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def clean_filename(filename: str) -> str:
    # remove special characters
    filename = re.sub(r"[^\w\-. ]", "", filename)

    # replace spaces with underscore
    filename = filename.replace(" ", "_")

    return filename


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    clean_name = clean_filename(file.filename)

    # add unique ID to prevent overwrites
    unique_name = f"{uuid4().hex}_{clean_name}"

    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "original_name": file.filename,
        "saved_as": unique_name
    }