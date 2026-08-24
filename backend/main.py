from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "CampusLens AI API is running"}