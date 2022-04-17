
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
from .model import RaceEvent, EnterEvent


#Note: uuid is the players uuid, timestamp is the last update to the player status, where timestamp refers to the app-time, not the server time.
class PlayerStatus(RaceEvent):
    enterEvent: EnterEvent
    lapsCompleted:int
    totalPoints:int
    bestLap: timedelta