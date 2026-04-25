from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from functools import lru_cache

from chat import *

app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    # "https://your-domain.com",  # Production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "CORS is configured!"}

class PredictRequest(BaseModel):
    message: str = ""

@lru_cache
@app.post("/predict")
async def predict(data: PredictRequest):
    text = data.message
    response = chat(text)
    return {"answer": response}

if __name__ == "__main__":
    uvicorn.run(app, port=5000)

