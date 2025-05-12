from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Reading(BaseModel):
    timestamp: datetime
    temperature: float = Field(..., ge=-50, le=60, description="Temp. in °C")
    pressure: int = Field(..., ge=800, le=1100, description="Pressure in hPa")
    humidity: float = Field(..., ge=0, le=100, description="Humidity %")
    pm10: Optional[float]
    pm25: Optional[float]


database: List[Reading] = []


@app.post("/readings/")
def add_reading(reading: Reading):
    database.append(reading)
    return {"message": "Reading added successfully"}


@app.get("/readings/nearest")
def get_nearest_reading(datetime_str: str = Query(..., alias="datetime")):
    try:
        target = datetime.fromisoformat(datetime_str)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid datetime format. Use ISO format (e.g. 2023-10-10T14:30:00)",
        )

    if not database:
        raise HTTPException(status_code=404, detail="No readings available")

    nearest = min(database, key=lambda r: abs(r.timestamp - target))
    return nearest


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)
