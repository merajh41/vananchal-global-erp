from fastapi import FastAPI
from app.config import settings
from app.database.init_db import init_db

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

@app.on_event("startup")
def startup():
    init_db()

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
    return {"status": "healthy"}
from app.routes.company import router as company_router

app.include_router(company_router)
from app.routes.auth import router as auth_router

app.include_router(auth_router)
from app.routes.company import router as company_router

app.include_router(company_router)
from app.routes.auth import router as auth_router

app.include_router(auth_router)
app.include_router(auth_router)