import os
import pickle

# Make sure folder exists
os.makedirs("ml", exist_ok=True)

# Save the model
pickle.dump(pipeline, open("ml/model.pkl", "wb"))

# Save the hourly aggregated CSV
hourly_df.to_csv("ml/hourly_aggregated.csv", index=False)


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load raw CSV
df = pd.read_csv("3Food_Delivery_Times.csv")

# Convert order time to hour
df["order_time"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce")
df["hour"] = df["order_time"].dt.hour

# Aggregate hourly
hourly_df = df.groupby(
    ["Day_of_Week", "hour", "Weather", "Vehicle_Type"]
).agg(
    orders_in_hour=("Order_ID", "count"),
    avg_prep_time=("Preparation_Time_min", "mean"),
    avg_delivery_time=("Delivery_Time_min", "mean")
).reset_index()

# Features & target
X = hourly_df[["Day_of_Week","hour","Weather","Vehicle_Type","avg_prep_time","orders_in_hour"]]
y = hourly_df["avg_delivery_time"]

# Preprocessing
categorical_cols = ["Day_of_Week","Weather","Vehicle_Type"]
numerical_cols = ["hour","avg_prep_time","orders_in_hour"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ("num", "passthrough", numerical_cols),
])

# Train pipeline
pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42))
])

pipeline.fit(X, y)

# Save pipeline to model.pkl
pickle.dump(pipeline, open("ml/model.pkl", "wb"))

# Save hourly aggregation for backend lookup
hourly_df.to_csv("ml/hourly_aggregated.csv", index=False)
