from fastapi import FastAPI

app = FastAPI(
    title="Vananchal Global ERP",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "company": "Vananchal Global ERP",
        "status": "Running Successfully",
        "version": "1.0.0"
    }