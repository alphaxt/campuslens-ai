from fastapi import FastAPI

app = FastAPI(
    title="CampusLens AI API",
    description="Backend API for CampusLens AI",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "CampusLens AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }