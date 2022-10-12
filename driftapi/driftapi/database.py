"""
Module providing uniform access to the database, taking care of generating unique IDs for the elements,
converting them back to their actual data types on retrieval, etc.
"""

from datetime import timedelta, timezone, datetime
import time
import uuid
from typing import List, Optional, TypeVar, Generic, cast, Any, Type, get_args
from collections.abc import Callable

from pymongo import MongoClient, DESCENDING, ASCENDING
from pydantic import BaseModel

from .model import RaceEvent, EnterEvent, StartEvent, TargetEvent, EndEvent, target_code
from .model_racedisplay import PlayerStatus, Game
from .singletons import settings, logger


T = TypeVar('T', bound=BaseModel)

    


class DbClient:
    """High-Level class for accessing the DB. Delegates to different client classes for the different concepts
    in the DB. Those client classes could also easily be swapped out for another library, e.g. async-mongo or SQL.
    This high-level class is not really necessary, but this way cou can have proper type-hints instead of just
    expecting and returning "BaseModel" all the time.
    """

    def __init__(self, mongo_client):
        db = mongo_client[settings.database_name]
        self.raceevent_db = PyMongoClient(db["raceevent"])
        self.playerstatus_db = GenericDbClient[PlayerStatus](db, PlayerStatus)
        self.game_db = GenericDbClient[Game](db, Game)

    def insert_raceevent(self, game_id:str, obj: RaceEvent, sha3_password = None) -> str:
        obj.game_id = game_id#for safety
        values = {**obj.dict(), "created_at": get_time(), "updated_at": get_time(), "class": type(obj).__name__}

        logger.info(type(obj).__name__)
        eventType = type(obj)
        if eventType is EnterEvent:
            logger.info("insert or update player status")
            self.insert_or_update_playerstatus(game_id, obj)
        elif eventType is TargetEvent:
            playerStatusId = self.playerstatus_db.find_one({'game_id':game_id, 'user_id':obj.user_id})
            playerStatus = self.playerstatus_db.get(playerStatusId)
            game = self.game_db.find_one_and_get({'game_id':game_id})

            #increase the target code counter by one (for tracking the number of targets that had been passed)
            playerStatus.target_code_counter[str(obj.data.target_code.value)]+=1

            #check if joker lap should be increased:

            if game.joker_lap_code == obj.data.target_code:
                if not game.joker_lap_precondition_code:
                    playerStatus.joker_laps_counter += 1
                    logger.info("Joker lap without precondition triggered")
                elif game.joker_lap_precondition_code == playerStatus.last_recognized_target:
                    playerStatus.joker_laps_counter += 1
                    logger.info("Joker lap with precondition triggered")
                else:
                    logger.info("no joker lap triggered because condition is not fullfilled (condition->status)")


            if obj.data.target_code == target_code.start_finish:
                if playerStatus.last_lap_timestamp:
                    playerStatus.laps_completed += 1 #only add a lap after the start line has been crossed the second time

                    new_lap_time:timedelta = obj.data.crossing_time.astimezone(timezone.utc) - playerStatus.last_lap_timestamp.astimezone(timezone.utc)
                    playerStatus.last_lap = str(new_lap_time.total_seconds())
                    if playerStatus.best_lap:
                        bestLap = timedelta(seconds=float(playerStatus.best_lap))
                        if bestLap > new_lap_time:
                            playerStatus.best_lap = str(new_lap_time.total_seconds())
                    else:
                        playerStatus.best_lap = str(new_lap_time.total_seconds())
                    playerStatus.last_lap_timestamp = obj.data.crossing_time
                else:
                    #this is only active when the target finished is crossed the first time, as in that case, there is no last_lap_timestamp set:
                    #for the first lap, we count the time since the signal time, not the first crossing. This is how it is done in the drift app.
                    playerStatus.last_lap_timestamp = playerStatus.start_data.signal_time

            if obj.data.score>0:
                playerStatus.total_score += int(obj.data.score)
                
            playerStatus.last_recognized_target = obj.data.target_code
            self.playerstatus_db.update(playerStatusId, playerStatus)
        elif eventType is StartEvent:
            playerStatusId = self.playerstatus_db.find_one({'game_id':game_id, 'user_id':obj.user_id})
            if playerStatusId:
                playerStatus = self.playerstatus_db.get(playerStatusId)
                playerStatus.start_data = obj.data
                self.playerstatus_db.update(playerStatusId, playerStatus)

        elif eventType is EndEvent:
            playerStatusId = self.playerstatus_db.find_one({'game_id':game_id, 'user_id':obj.user_id})
            if playerStatusId:
                playerStatus = self.playerstatus_db.get(playerStatusId)
                playerStatus.end_data = obj.data

                if playerStatus.start_data and playerStatus.end_data:
                    totalRaceTime:timedelta = playerStatus.end_data.finished_time.astimezone(timezone.utc) - playerStatus.start_data.signal_time.astimezone(timezone.utc)
                    playerStatus.total_time = str(totalRaceTime.total_seconds())
                playerStatus.total_score = playerStatus.end_data.total_score
                self.playerstatus_db.update(playerStatusId, playerStatus)

        self.raceevent_db.insert(values)
        return "OK"#self.raceevent_db.insert(values)
    
    def update_raceevent(self, id_: str, raceevent: RaceEvent) -> bool:
        values = {**raceevent.dict(), "updated_at": get_time()}
        return self.raceevent_db.update(id_, values)

    def delete_raceevent(self, id_: str) -> bool:
        return self.raceevent_db.delete(id_)

    def get_raceevent(self, id_: str) -> Optional[RaceEvent]:
        res = self.raceevent_db.get(id_)
        cls = globals()[res["class"]]
        return res and _convert(res, cls)
    
    def find_raceevent(self, query:dict) -> List[RaceEvent]:
        res = self.raceevent_db.find(query)
        return res and [_convert(x, globals()[x["class"]]) for x in res]
    

    def get_scoreboard(self, game_id:str) -> List[PlayerStatus]:
        query = {"game_id":game_id}
        return self.playerstatus_db.find_and_get(query)

    def insert_or_update_playerstatus(self, game_id:str, obj: EnterEvent) -> bool:
        targetCounter = {}
        for e in target_code:
            targetCounter[str(e.value)]=0

        playerStatus = PlayerStatus(
            game_id = obj.game_id,
            user_id = obj.user_id,
            user_name = obj.user_name,
            laps_completed = 0,
            total_score = 0,
            total_time = "",
            last_lap = None,
            best_lap = None,
            target_code_counter=targetCounter,
            last_recognized_target = None,
            joker_laps_counter = 0,
            enter_data = obj.data,
            start_data = None,
            end_data = None
        )

        oldPlayerId = self.playerstatus_db.find_one(query={"game_id":game_id, "user_id":obj.user_id})
        if oldPlayerId:
            #if the player already existed, use the new, reset data but keep the best lap.
            oldPlayer = self.playerstatus_db.find_one_and_get(query={"game_id":game_id, "user_id":obj.user_id})
            #playerStatus.best_lap = oldPlayer.best_lap

            self.playerstatus_db.update(oldPlayerId, playerStatus)
        else:
            self.playerstatus_db.insert(playerStatus)
        return True


    def list_playerstati(self, game_id:str) -> List[PlayerStatus]:
        query = {"game_id":game_id}
        return self.playerstatus_db.find_and_get(query)


class PyMongoClient:
    """Low-Level DB Client for pymongo (synchronous)"""

    def __init__(self, db):
        self.db = db

    def insert(self, obj: dict) -> str:
        res = self.db.insert_one({"_id": uuid.uuid4(), **obj})
        return str(res.inserted_id)

    def get(self, id_: str) -> Optional[dict]:
        return self.db.find_one({"_id": uuid.UUID(str(id_))})

    def find(self, values: dict) -> dict:
        return self.db.find(values)

    def find_one(self, values: dict) -> dict:
        return self.db.find_one(values)

    def update(self, id_: str, values: dict) -> bool:
        res = self.db.update_one({"_id": uuid.UUID(str(id_))}, {"$set": values})
        return res.modified_count == 1

    def delete(self, id_: str) -> bool:
        res = self.db.delete_one({"_id": uuid.UUID(str(id_))})
        return res.deleted_count == 1


#helper methods
def get_time() -> int:
    """Just a helper for getting time in consistent way"""
    return int(time.time())

def _convert(obj: dict, cls: type):
    """Remove redundant _id field and convert to given type."""
    if obj is not None:
        obj["id"] = str(obj["_id"])
        del obj["_id"]
        return cls(**obj)

class GenericDbClient(Generic[T]):
    db:PyMongoClient
    cls:type

    def __init__(self, mongo_client, cls:type):
        db = mongo_client[settings.database_name]
        self.db = PyMongoClient(db[T.__name__])
        self.cls = cls


    def insert(self, obj:T) -> str:
        values = {**obj.dict(), "created_at": get_time(), "updated_at": get_time(), "class": type(obj).__name__}
        return self.db.insert(values)

    def update(self, id_: str, obj: T) -> bool:
        values = {**obj.dict(), "updated_at": get_time()}
        return self.db.update(id_, values)

    def delete(self, id_: str) -> bool:
        return self.db.delete(id_)

    def get(self, id_: str) -> Optional[T]:
        res = self.db.get(id_)
        return res and _convert(res, self.cls)

    def find(self, query:dict) -> Optional[List[str]]:
        query['class'] = self.cls.__name__
        res = self.db.find(query)
        if res is not None:
            return [r['_id'] for r in res]

    def find_and_get(self, query:dict) -> Optional[List[T]]:
        query['class'] = self.cls.__name__
        res = self.db.find(query)
        if res is not None:
            return [_convert(r, self.cls) for r in res]

    def find_one(self, query:dict) -> Optional[str]:
        query['class'] = self.cls.__name__
        res = self.db.find_one(query)
        if res is not None:
            return res['_id']

    def find_one_and_get(self, query:dict) -> Optional[T]:
        query['class'] = self.cls.__name__
        res = self.db.find_one(query)
        if res is not None:
            return _convert(res, self.cls)


# Singleton instance
def create_db_client():
    mongo_database_url = settings.database_url
    mongo_client = MongoClient(mongo_database_url)
    return DbClient(mongo_client)


db_client = create_db_client()
