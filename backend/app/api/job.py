from fastapi import APIRouter
from pydantic import BaseModel

from app.services.skill_extractor import extract_skills

router = APIRouter()


class JobDescriptionRequest(BaseModel):
    job_description: str


@router.post("/analyze-job")
def analyze_job(data: JobDescriptionRequest):

    skills = extract_skills(data.job_description)

    return {
        "skills": skills,
        "total_skills_found": len(skills)
    }