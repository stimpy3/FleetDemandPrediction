# train.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# ------------------------------
# Paths
# ------------------------------
ml_folder = "ml"
csv_file = os.path.join(ml_folder, "3Food_Delivery_Times.csv")
model_file = os.path.join(ml_folder, "model.pkl")
hourly_file = os.path.join(ml_folder, "hourly_aggregated.csv")

# Make sure ml folder exists
os.makedirs(ml_folder, exist_ok=True)

# ------------------------------
# Load CSV
# ------------------------------
df = pd.read_csv(csv_file)

# Convert order time to hour
df["order_time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce")
df["hour"] = df["order_time"].dt.hour

# ------------------------------
# Aggregate hourly
# ------------------------------
hourly_df = df.groupby(
    ["Day_of_Week", "hour", "Weather", "Vehicle_Type"]
).agg(
    orders_in_hour=("Order_ID", "count"),
    avg_prep_time=("Preparation_Time_min", "mean"),
    avg_delivery_time=("Delivery_Time_min", "mean")
).reset_index()

# ------------------------------
# Features & target
# ------------------------------
X = hourly_df[["Day_of_Week","hour","Weather","Vehicle_Type","avg_prep_time","orders_in_hour"]]
y = hourly_df["avg_delivery_time"]

# ------------------------------
# Preprocessing
# ------------------------------
categorical_cols = ["Day_of_Week","Weather","Vehicle_Type"]
numerical_cols = ["hour","avg_prep_time","orders_in_hour"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ("num", "passthrough", numerical_cols),
])

# ------------------------------
# Train pipeline
# ------------------------------
pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42))
])

pipeline.fit(X, y)

# ------------------------------
# Save model & hourly aggregation
# ------------------------------
pickle.dump(pipeline, open(model_file, "wb"))
hourly_df.to_csv(hourly_file, index=False)

print(f"Training complete! Files saved in {ml_folder}/")
