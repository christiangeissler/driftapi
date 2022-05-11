from fastapi import FastAPI, HTTPException
from typing import Optional


from . import __version__
from .singletons import settings, logger
from .database import db_client
from .model import EndEvent, EnterEvent, StartEvent, TargetEvent, EndEvent
from .model_racedisplay import PlayerStatus, Game

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
@app.get("/game/{game_id}/ping", status_code=200)
async def ping(game_id:str, sha3_password: Optional[str] = None):

    game = db_client.game_db.find_one_and_get({"game_id":game_id})
    if game:
        reply = {"status": True}
        if game.start_time: reply["start_time"] = game.start_time
        if game.lap_count: reply["lap_count"] = game.lap_count
        if game.track_condition: reply["track_condition"] = game.track_condition
        if game.track_bundle: reply["track_bundle"] = game.track_bundle
        if game.wheels: reply["wheels"] = game.wheels
        if game.setup_mode: reply["setup_mode"] = game.setup_mode
        return reply
    raise HTTPException(status_code=404, detail="Item not found")


# This event is triggered when the user starts a run (free run, race, gymkhana) and after the loading is completed (the user sees the hud of the racer)
# it's purpose is for the server to control the car setup and if that matches with what is allowed for the race
@app.post("/game/{game_id}/enter", status_code=201)
async def create_EnterEvent(game_id:str, enterEvent:EnterEvent, sha3_password: Optional[str] = None):
    return db_client.insert_raceevent(game_id, enterEvent, sha3_password)

# This event is triggered when the user hits the "Start Motor" button the first time.
@app.post("/game/{game_id}/start", status_code=201)
async def create_StartEvent(game_id:str, startEvent:StartEvent, sha3_password: Optional[str] = None):
    return db_client.insert_raceevent(game_id, startEvent, sha3_password)

# This event is triggered whenever a target is recognized
@app.post("/game/{game_id}/target", status_code=201)
async def create_TargetEvent(game_id:str, targetEvent:TargetEvent, sha3_password: Optional[str] = None):
    return db_client.insert_raceevent(game_id, targetEvent, sha3_password)

# This event is triggered whenever a player shuts down the motor and finishes the run
@app.post("/game/{game_id}/end", status_code=201)
async def create_EndEvent(game_id:str, endEvent:EndEvent, sha3_password: Optional[str] = None):
    return db_client.insert_raceevent(game_id, endEvent, sha3_password)

if settings.enable_racedisplay:

    # This is a debug function that you can use to query for the created race events.
    @app.put("/game/{game_id}/events", status_code=200)
    async def get_Events(game_id:str, query:dict):
        query["game_id"]=game_id
        return db_client.find_raceevent(query)

    @app.get("/game/{game_id}/playerstatus", status_code=200)
    async def get_scoreboard(game_id:str):
        result = db_client.playerstatus_db.find_and_get(query={'game_id':game_id})
        if result:
            return result
        raise HTTPException(status_code=404, detail="a game with that id was not found")

    @app.post("/manage_game/create", status_code=201)
    async def create_game(game:Game):
        logger.info("create game")
        if db_client.game_db.find_one({"game_id":game.game_id}):
            raise HTTPException(status_code=409, detail="A game with that id already exists. Delete the game and then try again.")
        return db_client.game_db.insert(game)

    @app.post("/manage_game/delete/{game_id}")
    async def delete_game():
        query = {"game_id":game_id}
        id = db_client.game_db.find_one(query)
        if id:
            return db_client.game_db.delete(id)
        raise HTTPException(status_code=404, detail="Item not found")

    @app.get("/manage_game/get/{game_id}/", status_code=200)
    async def get_game(game_id:str):
        return db_client.game_db.find_one_and_get(query = {"game_id":game_id})

    @app.post("/manage_game/find/")
    async def find_game(query:dict):
        return db_client.game_db.find_and_get(query)
