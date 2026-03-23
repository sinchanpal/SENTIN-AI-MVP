from fastapi import FastAPI
from routers import text_scanner
from routers import url_scanner

#! to run this file use command : uvicorn main:app --reload
app = FastAPI(title="SENTIN-AI Backend API")


# Connect the separate tracks to the main station!
app.include_router(text_scanner.router, prefix="/api")
app.include_router(url_scanner.router, prefix="/api")

@app.get("/")
def home():
    return {"message": "SENTIN-AI Python Engine is Active"}
