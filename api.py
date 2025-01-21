from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import joblib
import numpy as np

app = FastAPI()
model = joblib.load('model.pkl')

# Instrumentateur Prometheus
Instrumentator().instrument(app).expose(app)

@app.post("/predict")
async def predict(features: list):
    prediction = model.predict([features])
    return {"prediction": int(prediction[0])}
