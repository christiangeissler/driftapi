
"""
Module defining the driftapi core and enum classes.
Note: for a complete server implementation, you probably want to also define some additional classes.

"""
from enum import Enum
from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ValidationError, Field


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

class RaceEvent(BaseModel):
    uuid: UUID = Field(None, title="unique user id", description="unique identifier (for the duration of the current race), can and should be different from the Sturmkind user name for legal and security reasons, for example a hash of the username or a hash of the devices ip address.")
    timestamp: datetime = Field(None, title="the exact timestamp down to the precision the sturmkind app uses, so fractions of a second")

class Barcode(str, Enum):
    finish = "FINISH"
    angledrift = "ANGLE"
    speeddrift = "SPEED"
    threesixty = "360"
    hundredeightyspeed = "180SPEED"

class EnterEvent(RaceEvent):
    username: str = Field(None, title="the name choosen by the user to be displayed on the scoreboard", description="Can be different from the Sturmkind user name (for legal reasons)")
    carname: str = Field(None, title="the name the user has given for the specific car (not always the same as the car type)")
    cartype: str = Field(None, title="The name of the car model, for example D1, 190 Evo II, etc., this is not an ENUM as new cars might be added in the future and we do not want to adjust the API every time that happens.")
    motortype: str = Field(None, title="The id of the motor type. No ENUM for the above reason. Example: 'DTM', 'V8' etc.") 
    motorsetup: str = Field(None, title="The id of the motor setup. No ENUM for the above reason. Example: 'DTM', 'V8' etc.")  #according to the app-internal id for the different motor setups. No ENUM for the above reason.
    carsetup:Carsetup #'DRIFT or RACE'
    trackproperty:Trackproperty #'DRY or WET or GRAVEL or ICE'
    tires:Tires #STREET, SPIKES, RALLY
    mode:Optional[str] = 'NONE' #NONE or RALLYCROSS
    laps:Optional[int] = 0
    driftassist:bool
    softsteering:bool

class StartMotorEvent(RaceEvent):
    pass

class BarcodeEvent(RaceEvent):
    barcode: Barcode
    #currentspeed: float #optional for a later implementation as discussed with martin
    #currentdriftangle: float #optional for a later implementation as discussed with martin
    #stage:Optional[int] = 0 #optional for a later implementation as discussed with martin

class PointReasons(str, Enum):
    earlystart = "EARLYSTART"
    angledrift = "ANGLE"
    speeddrift = "SPEED"
    threesixty = "360"
    hundredeightyspeed = "180SPEED"
    intimefinish = "INTIMEFINISH"

class PointsAwardedEvent(RaceEvent):
    points:int
    pointsTotal:int
    reason:PointReasons
    combo:Optional[bool] = False
    supercombo:Optional[bool] = False

# This event is triggered whenever the user leaves a run (shutting down the motor)
class FinishEvent(RaceEvent):
    pass