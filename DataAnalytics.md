__1️⃣ Modifications to the dataset__

“I made controlled modifications to enrich the dataset for modeling and simulation:

1. Added a Day_of_Week column using realistic probabilities:
   df['Day_of_Week'] = np.random.choice(days, size=len(df), p=day_probs)

2. Converted coarse Time_of_Day buckets into exact hours and minutes for continuous time:
  df['Hour'], df['Minute'] = df['Time_of_Day'].apply(generate_time).str

3. Split the timestamp into separate Date and Time columns:
   df['Date'] = timestamp.dt.date
   df['Time'] = timestamp.dt.time

4. Removed all rows with Vehicle_Type = 'Car' as they were outside the scope:
   df = df[df['Vehicle_Type'] != 'Car']

These changes preserved realistic patterns while making the dataset slider and model-ready.”

---

__2️⃣ Exploratory Data Analysis (EDA)__

“For EDA, I performed:

1. Checked for missing values and handled them:
   df['Time_of_Day'].fillna(np.random.choice(time_buckets, size=missing_count, p=probs))

2. Examined distributions of orders across time and day:
   df['Time_of_Day'].value_counts(normalize=True)   
   df['Day_of_Week'].value_counts(normalize=True)

3. Verified numerical ranges for columns like Distance_km and Delivery_Time_min:
   df.describe()

4. Checked categorical distributions for Weather, Traffic_Level, Vehicle_Type to ensure balance.
   This EDA guided both the data enrichment and model design for fleet prediction.”

---

__3️⃣ Optional bonus__
If they probe about “why you enriched data”:
“The original dataset was coarse in time, which would have limited both the model’s predictions and the slider visualization. By adding exact timestamps and day-of-week simulation, we could create hour-level demand predictions and realistic fleet simulations.”