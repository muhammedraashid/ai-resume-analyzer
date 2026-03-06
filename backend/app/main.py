from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Resume Analyzer")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is running"}


from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.job import router as job_router

app = FastAPI()

app.include_router(upload_router, prefix="/api")
app.include_router(job_router, prefix="/api")