from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import pickle
import numpy as np
import os

# Create FastAPI app
app = FastAPI(
    title=" Prediction",   
    description="Predict the irrigation status of a plant",
)

## this allow the testing locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during testing
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load our trained model
try:
    MODEL_PATH = "decision_tree_model.pkl"
    model = pickle.load(open(MODEL_PATH, 'rb'))
except Exception as e:
    print(f"Error loading model: {e}")

class WeatherInput(BaseModel):
    soil_moisture: float
    temperature: float
    soil_humidity: float
    time: float
    air_temperature: float
    wind_speed: float
    air_humidity: float
    wind_gust: float
    pressure: float

@app.post("/predict")
async def predict_status(data: WeatherInput):
    try:
        features = np.array([[
            data.soil_moisture,
            data.temperature,
            data.soil_humidity,
            data.time,
            data.air_temperature,
            data.wind_speed,
            data.air_humidity,
            data.wind_gust,
            data.pressure
        ]])
        
        prediction = model.predict(features)[0]
        
        return {
            "status": prediction,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def home():
    return {
        "message": "Welcome to Mahiri Irrigation Prediction App!",
        "docs_url": "/docs",
        "health_check": "/health"
}