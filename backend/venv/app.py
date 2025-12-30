from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Fleet Demand Forecast API is running"}