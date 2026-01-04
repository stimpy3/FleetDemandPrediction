# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------
# Load trained model
# ------------------------------
pipeline = pickle.load(open("ml/model.pkl", "rb"))

# Load historical hourly aggregated data
hourly_df = pd.read_csv("ml/hourly_aggregated.csv")

# ------------------------------
# Initialize FastAPI app
# ------------------------------
app = FastAPI(title="Fleet Predictor API")


# Optional: allow frontend to call API from other ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Define request payload
# ------------------------------
class PredictPayload(BaseModel):
    Day_of_Week: str
    Weather: str
    Traffic_Level: str
    Vehicle_Type: str
    avg_prep_time: float

# ------------------------------
# API Endpoint: predict fleet hourly
# ------------------------------
@app.post("/predict-hourly")
def predict_hourly(payload: PredictPayload):
    day = payload.Day_of_Week
    weather = payload.Weather
    traffic = payload.Traffic_Level
    vehicle = payload.Vehicle_Type
    avg_prep_time = payload.avg_prep_time

    results = []

    for hour in range(9, 22):  # 9am → 9pm
        hist = hourly_df[
            (hourly_df["Day_of_Week"] == day) &
            (hourly_df["hour"] == hour) &
            (hourly_df["Vehicle_Type"] == vehicle)
        ]

        orders = int(hist["orders_in_hour"].mean()) if not hist.empty else 20

        X_input = pd.DataFrame([{
            "Day_of_Week": day,
            "hour": hour,
            "Weather": weather,
            "Vehicle_Type": vehicle,
            "avg_prep_time": avg_prep_time,
            "orders_in_hour": orders
        }])

        pred_delivery = pipeline.predict(X_input)[0]
        fleet = np.ceil((orders * pred_delivery) / 60)

        results.append({
            "hour": hour,
            "fleet_required": int(fleet),
             "orders_in_hour": int(orders) 
         
        })

    return {"predictions": results}

# ------------------------------
# Run with: uvicorn app:app --reload
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
