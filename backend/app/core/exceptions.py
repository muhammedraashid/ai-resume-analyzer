from fastapi import HTTPException


class UnsupportedFileException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, 
            detail="Unsupported file format. only PDF and DOCX formats allowed."
        )

class ResumeParsingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=500,
            detail="Failed to parse resume."
        )