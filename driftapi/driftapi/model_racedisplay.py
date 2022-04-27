
"""
Module defining the driftapi core and enum classes.
Note: for a complete server implementation, you probably want to also define some additional classes.

"""
from enum import Enum
from time import time
from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta

from pydantic import BaseModel, ValidationError, Field
#from .model import RaceEvent, EnterEvent


class Game(BaseModel):
    game_id:str
    password_sh3:Optional[str]
    start_time:Optional[datetime]

    track_id:Optional[str]

    time_limit:Optional[float] = Field(None, title="the time limit for the run, in seconds")
    lap_count:Optional[int] = Field(None, title="number of rounds (for the race mode)")
    #future: add more conditions (race conditions)




#Note: uuid is the players uuid, timestamp is the last update to the player status, where timestamp refers to the app-time, not the server time.
class PlayerStatus(BaseModel):
    game_id:str
    user_id:UUID
    user_name:str
    laps_completed:int
    total_points:int
    best_lap: str