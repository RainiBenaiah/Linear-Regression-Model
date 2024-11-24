from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import pickle
import numpy as np
import os
import sklearn
import sys

# Create FastAPI app
app = FastAPI(
    title="Irrigation Prediction",   
    description="Predict the irrigation status of a plant",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during testing
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event logging
@app.on_event("startup")
async def startup_event():
    print(f"Python version: {sys.version}")
    print(f"NumPy version: {np.__version__}")
    print(f"Scikit-learn version: {sklearn.__version__}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")

# Load the model with enhanced error handling
try:
    MODEL_PATH = "decision_tree_model.pkl"
    with open(MODEL_PATH, 'rb') as f:
        print(f"Attempting to load model from {os.path.abspath(MODEL_PATH)}")
        model = pickle.load(f)
except FileNotFoundError:
    print(f"Model file not found at {os.path.abspath(MODEL_PATH)}")
    model = None
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

# Input data model
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

# Prediction endpoint
@app.post("/predict")
async def predict_status(data: WeatherInput):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded. Please check server logs."
        )
    
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
        ]], dtype=np.float32)  # Explicitly specify dtype
        
        prediction = model.predict(features)[0]
        return {
            "status": prediction,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Home endpoint
@app.get("/")
async def home():
    return {
        "message": "Welcome to Mahiri Irrigation Prediction App!",
        "docs_url": "/docs",
        "health_check": "/health"
    }

# Health check endpoint
@app.get("/health")
async def health():
    return {
        "status": "OK",
        "model_loaded": model is not None
    }

# Debug section for local testing
if __name__ == "__main__":
    if model is not None:
        # Test with sample data
        test_data = np.array([[
            50,  # soil_moisture
            25,  # temperature
            60,  # soil_humidity
            12,  # time
            23,  # air_temperature
            10,  # wind_speed
            70,  # air_humidity
            15,  # wind_gust
            101  # pressure
        ]], dtype=np.float32)
        
        print("Test prediction:", model.predict(test_data))
