from fastapi import FastAPI, HTTPException
from typing import Optional

from . import __version__
from .singletons import settings, logger
from .database import db_client
from .model import EndEvent, EnterEvent, RaceEvent, StartEvent, TargetEvent, EndEvent, PingResponse
from .model_racedisplay import PlayerStatus, Game

tags_metadata = [
    {
        "name": "community_api",
        "description": "<p>part of the dr!ft community api</p>",
    },
    {
        "name": "racingserver_api",
        "description": "<p>NOT part of the dr!ft community api</p>",
    },
]

# create App
app = FastAPI(
    title="driftapi reference implementation",
    version=__version__,
    redoc_url=None,
    openapi_url="/openapi.json" if not settings.disable_openapi else "",
    openapi_tags=tags_metadata,
    root_path=settings.root_path,
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# This event is triggered when a user enters a server uri in the app. The app can see if there actually is a server behind that uri and could for example show a green light, so that the user knows he entered the right server.
@app.get("/game/{game_id}/ping", status_code=200, response_model = PingResponse, tags=["community_api"], description="Ping that is used from the app to determine if a race with this uri and race id exists. The response is used to synchronize the race settings in the app, see example response. All fields in the response are optional.")
async def ping(game_id:str):

    game = db_client.game_db.find_one_and_get({"game_id":game_id})
    if game:
        reply = {"status": True}
        if game.start_time: reply["start_time"] = game.start_time
        if game.start_delay: reply["start_delay"] = game.start_delay
        if game.lap_count: reply["lap_count"] = game.lap_count
        if game.track_condition: reply["track_condition"] = game.track_condition
        if game.track_bundle: reply["track_bundle"] = game.track_bundle
        if game.wheels: reply["wheels"] = game.wheels
        if game.setup_mode: reply["setup_mode"] = game.setup_mode
        return reply
    raise HTTPException(status_code=404, detail="Item not found")


# This event is triggered when the user starts a run (free run, race, gymkhana) and after the loading is completed (the user sees the hud of the racer)
# it's purpose is for the server to control the car setup and if that matches with what is allowed for the race
@app.post("/game/{game_id}/enter", status_code=201, tags=["community_api"], description="<p>This event is triggered when the user starts a run (free run, race, gymkhana) and after the loading is completed (the user sees the hud of the racer)</p><p>it's purpose is for the server to control the car setup and if that matches with what is allowed for the race</p>")
async def create_EnterEvent(game_id:str, enterEvent:EnterEvent):
    return db_client.insert_raceevent(game_id, enterEvent)

# This event is triggered when the user hits the "Start Motor" button the first time.
@app.post("/game/{game_id}/start", status_code=201, tags=["community_api"], description="This event is triggered when the user hits the 'Start Motor' button the first time.")
async def create_StartEvent(game_id:str, startEvent:StartEvent):
    return db_client.insert_raceevent(game_id, startEvent)

# This event is triggered whenever a target is recognized
@app.post("/game/{game_id}/target", status_code=201, tags=["community_api"], description="This event is triggered whenever a target is recognized")
async def create_TargetEvent(game_id:str, targetEvent:TargetEvent):
    return db_client.insert_raceevent(game_id, targetEvent)

# This event is triggered whenever a player shuts down the motor and finishes the run
@app.post("/game/{game_id}/end", status_code=201, tags=["community_api"], description = "This event is triggered whenever a player shuts down the motor and finishes the run")
async def create_EndEvent(game_id:str, endEvent:EndEvent):
    return db_client.insert_raceevent(game_id, endEvent)

if settings.enable_racedisplay:
    # All of the below functions belong to the reference racing server and are not part of the actual Dr!ft Community API.

    @app.get("/", tags=["racingserver_api"], description="Entry endpoint that directs to the openapi docs.")
    async def root():
        return {"message": "Welcome to the Sturmkind Dr!ft Community API & Reference Racing Server API. To see the available api calls, visit /docs."}

    # This is a debug function that you can use to query for the created race events.
    @app.put("/game/{game_id}/events", status_code=200, tags=["racingserver_api"], description="This is a debug function that you can use to query for the created race events.")
    async def get_Events(game_id:str, query:dict):
        query["game_id"]=game_id
        return db_client.find_raceevent(query)

    @app.get("/game/{game_id}/playerstatus", status_code=200, tags=["racingserver_api"])
    async def get_scoreboard(game_id:str):
        result = db_client.playerstatus_db.find_and_get(query={'game_id':game_id})
        return result

    @app.post("/manage_game/create", status_code=201, tags=["racingserver_api"])
    async def create_game(game:Game):
        logger.info("create game")
        if db_client.game_db.find_one({"game_id":game.game_id}):
            raise HTTPException(status_code=409, detail="A game with that id already exists. Delete the game and then try again.")
        return db_client.game_db.insert(game)

    @app.get("/manage_game/delete/{game_id}", status_code=200, tags=["racingserver_api"])
    async def delete_game(game_id:str):
        query = {"game_id":game_id}
        id = db_client.game_db.find_one(query)
        if id:
            query = {"game_id":game_id}#need a new dict
            idsOfPlayerstatiInGame = db_client.playerstatus_db.find(query)
            for playerstatus_id in idsOfPlayerstatiInGame:
                db_client.playerstatus_db.delete(playerstatus_id)
            return db_client.game_db.delete(id)
        raise HTTPException(status_code=404, detail="Item not found")

    @app.get("/manage_game/reset/{game_id}", status_code=200, tags=["racingserver_api"])
    async def reset_game(game_id:str):
        query = {"game_id":game_id}
        idsOfPlayerstatiInGame = db_client.playerstatus_db.find(query)
        for playerstatus_id in idsOfPlayerstatiInGame:
            db_client.playerstatus_db.delete(playerstatus_id)
        return

    @app.get("/manage_game/reset_player/{game_id}/{user_name}", status_code=200, tags=["racingserver_api"])
    async def reset_player(game_id:str, user_name:str):
        query = {"game_id":game_id, "user_name":user_name}#need a new dict
        idsOfPlayerstatiInGame = db_client.playerstatus_db.find(query)
        for playerstatus_id in idsOfPlayerstatiInGame:
            db_client.playerstatus_db.delete(playerstatus_id)
        return

    @app.get("/manage_game/get/{game_id}/", status_code=200, tags=["racingserver_api"])
    async def get_game(game_id:str):
        return db_client.game_db.find_one_and_get(query = {"game_id":game_id})

    @app.post("/manage_game/find/", tags=["racingserver_api"])
    async def find_game(query:dict):
        return db_client.game_db.find_and_get(query)
