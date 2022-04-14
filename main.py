from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

class Barcode(str, Enum):
    finish = "FINISH"
    angledrift = "ANGLE"
    speeddrift = "SPEED"
    threesixty = "360"
    hundredeightyspeed = "180SPEED"

class Carsetup(str, Enum):
    drift = "DRIFT"
    race = "RACE"

class Trackproperty(str, Enum):
    dry = "DRY"
    wet = "WET"
    gravel = "GRAVEL"
    ice = "ICE"

class Tires(str, Enum):
    street = "STREET"
    spikes = "SPIKES"
    rally = "RALLY"


class RacerEvent(BaseModel):
    uuid: UUID #user name in drift app
    timestamp: datetime

# This event is triggered when a user enters a server uri in the app. The app can see if there actually is a server behind that uri and could for example show a green light, so that the user knows he entered the right server.
class HelloEvent(RacerEvent):
    pass

# This event is triggered when the user hits the "Start Motor" button the first time.
class StartMotorEvent(RacerEvent):
    pass

# This event is triggered whenever a target is recognized or a new measurement of a multi-measurement barcode is triggered (180 speed or 360), in which case the stage parameter is provided, starting from 0
class BarcodeEvent(RacerEvent):
    barcode: Barcode
    currentspeed: float
    currentdriftangle: float
    stage:Optional[int] = 0


# Optional Advanced Events:

# This event is triggered when the user starts a run (free run, race, gymkhana) and after the loading is completed (the user sees the hud of the racer)
# it's purpose is for the server to control the car setup and if that matches with what is allowed for the race
class EnterEvent(RacerEvent):
    carname: str #Whatever the user choosed
    cartype: str #according to the app-internal id for the different car types. No ENUM because we do not want to adjust this every time a new model comes out
    motortype: str #according to the app-internal id for the different motor types. No ENUM for the above reason.
    motorsetup: str #according to the app-internal id for the different motor setups. No ENUM for the above reason.
    carsetup:Carsetup #'DRIFT or RACE'
    trackproperty:Trackproperty #'DRY or WET or GRAVEL or ICE'
    tires:Tires #STREET, SPIKES, RALLY
    mode:Optional[str] = 'NONE' #NONE or RALLYCROSS
    rounds:Optional[int] = 0
    driftassist:bool
    softsteering:bool

class PointReasons(str, Enum):
    earlystart = "EARLYSTART"
    angledrift = "ANGLE"
    speeddrift = "SPEED"
    threesixty = "360"
    hundredeightyspeed = "180SPEED"
    intimefinish = "INTIMEFINISH"

# This event is triggered whenever the app awards the user with points (also for negative points or in-time-finish)
class PointsAwardedEvent(RacerEvent):
    points:int
    pointsTotal:int
    reason:PointReasons
    combo:Optional[bool] = False
    supercombo:Optional[bool] = False
    

# This event is triggered whenever the user leaves a run (shutting down the motor)
class FinishEvent(RacerEvent):
    pass


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Dr!ft API Demo. To see the available api calls, visit /docs."}

@app.post("/event/startmotor")
async def create_StartMotorEvent(startMotorEvent:StartMotorEvent):
    return startMotorEvent

@app.post("/event/barcode")
async def create_BarcodeEvent(barcodeEvent:BarcodeEvent):
    return barcodeEvent

@app.post("/event/enter")
async def create_BarcodeEvent(enterEvent:EnterEvent):
    return enterEvent

@app.post("/event/points")
async def create_BarcodeEvent(pointsAwardedEvent:PointsAwardedEvent):
    return pointsAwardedEvent