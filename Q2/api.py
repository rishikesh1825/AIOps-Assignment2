import time
import redis
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

redis_client = redis.Redis(host='cache', port=6379, db=0, decode_responses=True)
model = joblib.load('spam_model.joblib')

class Message(BaseModel):
    text: str

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(msg: Message):
    start_time = time.time()
    
    cached_result = redis_client.get(msg.text)
    if cached_result:
        return {"label": cached_result, "source": "cache", "time_ms": (time.time() - start_time) * 1000}
        
    prediction = model.predict([msg.text])[0]
    
    redis_client.setex(msg.text, 60, prediction)
    
    return {"label": prediction, "source": "model", "time_ms": (time.time() - start_time) * 1000}
