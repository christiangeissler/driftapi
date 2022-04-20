from fastapi import FastAPI, HTTPException
from typing import Optional


from . import __version__
from .singletons import settings
from .database import db_client
from .model import EnterEvent, StartMotorEvent, BarcodeEvent, PointsAwardedEvent, FinishEvent
from .model_racedisplay import PlayerStatus

# create App
app = FastAPI(
    title="driftapi reference implementation",
    version=__version__,
    redoc_url=None,
    openapi_url="/openapi.json" if not settings.disable_openapi else "",
    root_path=settings.root_path,
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Sturmkind Dr!ft Multiplayer Racing API. To see the available api calls, visit /docs."}

# This event is triggered when a user enters a server uri in the app. The app can see if there actually is a server behind that uri and could for example show a green light, so that the user knows he entered the right server.
@app.post("/{race_id}/ping")
async def ping(race_id:str, sha3_password: Optional[str] = None):
    return {"message": "Welcome! There is a server with a race ready and waiting for your events."}

# This event is triggered when the user starts a run (free run, race, gymkhana) and after the loading is completed (the user sees the hud of the racer)
# it's purpose is for the server to control the car setup and if that matches with what is allowed for the race
@app.post("/{race_id}/events/enter")
async def create_EnterEvent(race_id:str, enterEvent:EnterEvent, sha3_password: Optional[str] = None):
    return db_client.insert_raceevent(race_id, enterEvent, sha3_password)

# This event is triggered when the user hits the "Start Motor" button the first time.
@app.post("/{race_id}/events/startmotor")
async def create_StartMotorEvent(race_id:str, startMotorEvent:StartMotorEvent, sha3_password: Optional[str] = None):
    return db_client.insert_raceevent(race_id, startMotorEvent, sha3_password)

# This event is triggered whenever a target is recognized
@app.post("/{race_id}/events/barcode")
async def create_BarcodeEvent(race_id:str, barcodeEvent:BarcodeEvent, sha3_password: Optional[str] = None):
    return db_client.insert_raceevent(race_id, barcodeEvent, sha3_password)

# This event is triggered whenever the app awards the user with points (also for negative points or in-time-finish)
@app.post("/{race_id}/events/points")
async def create_PointsAwardedEvent(race_id:str, pointsAwardedEvent:PointsAwardedEvent, sha3_password: Optional[str] = None):
    return db_client.insert_raceevent(race_id, pointsAwardedEvent, sha3_password)

# This event is triggered whenever a player shuts down the motor and finishes the run
@app.post("/{race_id}/events/finish")
async def create_FinishEvent(race_id:str, finishEvent:FinishEvent, sha3_password: Optional[str] = None):
    return db_client.insert_raceevent(race_id, finishEvent, sha3_password)

if settings.enable_racedisplay:

    # This is a debug function that you can use to query for the created race events.
    @app.put("/{race_id}/events")
    async def get_Events(race_id:str, query:dict):
        query["race"]=race_id
        return db_client.find_raceevent(query)

    @app.put("/{race_id}/")
    async def get_scoreboard(race_id:str):
        return db_client.get_scoreboard(race_id)
