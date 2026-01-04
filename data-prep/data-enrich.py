import pandas as pd
import numpy as np
import random

# Load the CSV containing past food delivery orders. This is the dataset we will enrich
# for simulation and model training purposes.
df = pd.read_csv("Food_Delivery_Times.csv")

# Assumption: Our fleet only handles certain vehicles (e.g., bikes, scooters).
# To keep the simulation realistic, we permanently remove all orders assigned to cars.
df = df[df["Vehicle_Type"] != "Car"].reset_index(drop=True)


# Assumption: Original dataset does not have day information.
# We simulate realistic day-level demand using probabilities.
# Example: slightly higher demand on weekends.
days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
day_probs = [0.10, 0.11, 0.12, 0.14, 0.18, 0.20, 0.15]
df["Day_of_Week"] = np.random.choice(days, size=len(df), p=day_probs)

# Original dataset has coarse or missing time buckets (Morning/Afternoon/Evening/Night).
# We fill NaNs probabilistically to reflect realistic order distribution throughout the day.
time_buckets = ["Night", "Morning", "Afternoon", "Evening"]
time_bucket_probs = [0.15, 0.30, 0.25, 0.30]
mask = df["Time_of_Day"].isna()
df.loc[mask, "Time_of_Day"] = np.random.choice(
    time_buckets,
    size=mask.sum(),
    p=time_bucket_probs
)


# Assumption: Model and slider require exact times, not coarse buckets.
# Map each bucket to a realistic hour range and randomly assign an hour + minute within that range.
time_ranges = {
    "Night": (20, 23),
    "Morning": (9, 11),
    "Afternoon": (12, 15),
    "Evening": (16, 19)
}

def generate_time(bucket):
    start, end = time_ranges[bucket]
    return random.randint(start, end), random.randint(0, 59)

times = df["Time_of_Day"].apply(generate_time)

df["_hour"] = times.str[0]
df["_minute"] = times.str[1]



# Assumption: Having separate Date and Time columns makes the dataset cleaner for modeling
# and for visualization sliders. We anchor the week starting on Monday, Jan 6, 2025.
base_date = pd.to_datetime("2025-01-06")  # Monday anchor

day_to_offset = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2,
    "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
}

timestamp = (
    base_date
    + pd.to_timedelta(df["Day_of_Week"].map(day_to_offset), unit="D")
    + pd.to_timedelta(df["_hour"], unit="h")
    + pd.to_timedelta(df["_minute"], unit="m")
)

df["Date"] = timestamp.dt.date
df["Time"] = timestamp.dt.time

# Remove intermediate hour and minute columns to keep dataset clean.
df.drop(columns=["_hour", "_minute"], inplace=True)

# Save the processed dataset as a new CSV. This file is ready for modeling
# and visualization. Original dataset remains untouched.
df.to_csv("Food_Delivery_Times_ENRICHED.csv", index=False)

print("Saved as Food_Delivery_Times_ENRICHED.csv")
