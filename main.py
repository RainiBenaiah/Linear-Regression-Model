from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import pickle
import numpy as np
import os

# Create FastAPI app
app = FastAPI(
    title=" Irrigation Prediction",   
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
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil Moisture (0-100%)")
    temperature: float = Field(..., ge=-50, le=50, description="Temperature (-50°C to 50°C)")
    soil_humidity: float = Field(..., ge=0, le=100, description="Soil Humidity (0-100%)")
    time: float = Field(..., ge=0, le=24, description="Time (0-24 hours)")
    air_temperature: float = Field(..., ge=-50, le=50, description="Air Temperature (-50°C to 50°C)")
    wind_speed: float = Field(..., ge=0, le=150, description="Wind Speed (0-150 Km/h)")
    air_humidity: float = Field(..., ge=0, le=100, description="Air Humidity (0-100%)")
    wind_gust: float = Field(..., ge=0, le=200, description="Wind Gust (0-200 Km/h)")
    pressure: float = Field(..., ge=80, le=120, description="Pressure (80-120 KPa)")

@app.post("/predict")
async def predict_status(data: WeatherInput):
    try:
        # Convert the data to a NumPy array for prediction
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

        # Return the prediction as JSON
        return {
            "status": prediction,
            "success": True
        }
        
    except Exception as e:
        # Handle exceptions and return an error message
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def home():
    # Return a welcome message and links to documentation and health check
    return {
        "message": "Welcome to Mahiri Irrigation Prediction App!",
        "docs_url": "/docs",
        "health_check": "/health"
}

@app.get("/health")
async def health():
    # Return a health check status
    return {"status": "OK"}
