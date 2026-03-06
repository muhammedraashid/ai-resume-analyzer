import spacy
import re

nlp = spacy.load("en_core_web_sm")

SKILL_SET = {
    "python",
    "fastapi",
    "django",
    "flask",
    "docker",
    "kubernetes",
    "postgresql",
    "mysql",
    "mongodb",
    "react",
    "node",
    "aws",
    "git",
    "linux",
    "machine learning",
    "data analysis",
    "pandas",
    "numpy",
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text: str):

    text = clean_text(text)

    doc = nlp(text)

    found_skills = set()

    for token in doc:
        if token.text in SKILL_SET:
            found_skills.add(token.text)

    return list(found_skills)

