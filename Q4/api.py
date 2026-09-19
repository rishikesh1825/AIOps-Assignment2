from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import joblib

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_models["pipeline"] = joblib.load("spam_model.joblib")
    yield
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

class TextRequest(BaseModel):
    text: str

@app.get("/healthz")
def healthz(response: Response):
    if "pipeline" in ml_models:
        return {"status": "ok", "version": "v2"}
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "model not loaded"}

@app.post("/predict")
def predict(request: TextRequest):
    prediction = ml_models["pipeline"].predict([request.text])[0]
    return {"label": prediction}
