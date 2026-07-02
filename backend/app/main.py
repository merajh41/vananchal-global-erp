from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

@app.get("/")
def home():
    return {
        "application": settings.APP_NAME,
        "company": settings.COMPANY_NAME,
        "status": "Running Successfully",
        "version": settings.VERSION
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }