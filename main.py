from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import json


app = FastAPI()


# Define the data model

class TripData(BaseModel):
    CC: int
    ACC: int
    Lane_Keep: int


class Trips(BaseModel):
    Trips: List[Dict[str, TripData]]


# File to store the data

JSON_FILE = "data.json"


# Helper function to read data from JSON file

def read_json():
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"Trips": []}


# Helper function to write data to JSON file

def write_json(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=2)


# GET endpoint to retrieve all trips


@app.get("/")

async def get_trips():
    return {"Message":"Hello World"}

@app.get("/trips", response_model=Trips)

async def get_trips():
    return read_json()


# PUT endpoint to update or create trips

@app.put("/trips", response_model=Trips)
async def update_trips(trips: Trips):
    write_json(trips.dict())
    return trips


# GET endpoint to retrieve a specific trip

@app.get("/trips/{trip_id}")

async def get_trip(trip_id: str):

    data = read_json()

    for trip in data["Trips"]:

        if trip_id in trip:

            return {trip_id: trip[trip_id]}

    raise HTTPException(status_code=404, detail="Trip not found")


# PUT endpoint to update or create a specific trip

@app.put("/trips/{trip_id}")

async def update_trip(trip_id: str, trip_data: TripData):
        
        data = read_json()

        for trip in data["Trips"]:

            if trip_id in trip:

                trip[trip_id] = trip_data.dict()
                write_json(data)
                return {trip_id: trip[trip_id]}


# If trip doesn't exist, create a new one

        new_trip = {trip_id: trip_data.dict()}

        data["Trips"].append(new_trip)

        write_json(data) 
        return new_trip

