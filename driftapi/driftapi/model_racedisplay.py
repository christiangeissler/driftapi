
"""
Module defining the driftapi core and enum classes.
Note: for a complete server implementation, you probably want to also define some additional classes.

"""
from pydantic import BaseModel, ValidationError, Field

from enum import Enum
from time import time
from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta
from .model import track_condition, track_bundle, wheels, setup_mode, EnterData, StartData, EndData, target_code


class Game(BaseModel):
    game_id:str
    #password_sh3:Optional[str]
    start_time:Optional[datetime]

    start_delay:Optional[float]

    track_id:Optional[str]

    time_limit:Optional[float] = Field(None, title="the time limit for the run, in seconds")
    lap_count:Optional[int] = Field(None, title="number of rounds (for the race mode)")
    #future: add more conditions (race conditions)
    
    track_condition:Optional[track_condition]
    track_bundle:Optional[track_bundle]
    wheels:Optional[wheels]
    setup_mode:Optional[setup_mode]

    joker_lap_code:Optional[int] = Field(None, title="if set, this target code counter is displayed to be used for joker-laps etc.")
    joker_lap_precondition_code:Optional[int] = Field(None, title="if set, this target code is required to be detected before the joker-lap code to count as actual joker lap.")
    







#Note: uuid is the players uuid, timestamp is the last update to the player status, where timestamp refers to the app-time, not the server time.
class PlayerStatus(BaseModel):
    game_id:str
    user_id:UUID
    user_name:str
    laps_completed:int
    target_code_counter:dict
    total_score:Optional[int]
    total_time:Optional[str]
    best_lap:Optional[str]
    last_lap:Optional[str]
    last_lap_timestamp:Optional[datetime]
    last_recognized_target:Optional[target_code]
    joker_laps_counter:Optional[int]
    enter_data:Optional[EnterData]
    start_data:Optional[StartData]
    end_data:Optional[EndData]

