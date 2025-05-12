from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import List, Optional


class Reading:
    def __init__(
        self,
        timestamp: datetime,
        temperature: float,
        air_quality: condecimal(max_digits=5, decimal_places=2),
    ):
        self.timestamp = timestamp
        self.temperature = temperature
        self.air_quality = air_quality


class ReadingService:
    def __init__(self):
        self.readings = []

    def add_reading(self, reading: Reading):
        self.readings.append(reading)

    def get_nearest_reading(self, target_time: datetime) -> Optional[Reading]:
        nearest_reading = min(
            self.readings, key=lambda r: abs(r.timestamp - target_time), default=None
        )
        return nearest_reading


app = FastAPI()


class AirQualityReading(BaseModel):
    timestamp: datetime
    temperature: float
    air_quality: condecimal(max_digits=5, decimal_places=2)


reading_service = ReadingService()


@app.post("/readings/")
async def create_reading(reading: AirQualityReading):
    reading_service.add_reading(Reading(**reading.dict()))
    return {"message": "Reading added successfully"}


@app.get("/readings/")
async def get_nearest_reading(target_datetime: datetime):
    reading = reading_service.get_nearest_reading(target_datetime)
    if reading:
        return {
            "timestamp": reading.timestamp,
            "temperature": reading.temperature,
            "air_quality": reading.air_quality,
        }
    else:
        raise HTTPException(
            status_code=404, detail="No reading found for the given time"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)
