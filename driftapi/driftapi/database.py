"""
Module providing uniform access to the database, taking care of generating unique IDs for the elements,
converting them back to their actual data types on retrieval, etc.
"""

from datetime import timedelta
import time
import uuid
from typing import List, Optional, TypeVar, Generic, cast, Any, Type, get_args
from collections.abc import Callable

from pymongo import MongoClient, DESCENDING, ASCENDING
from pydantic import BaseModel

from .model import RaceEvent, EnterEvent, StartEvent, TargetEvent, EndEvent
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
        self.playerstatus_db = PyMongoClient(db["playerstatus"])
        self.game_db = GenericDbClient[Game](db, Game)

    def insert_raceevent(self, game_id:str, obj: RaceEvent, sha3_password = None) -> str:
        obj.game_id = game_id#for safety
        values = {**obj.dict(), "created_at": get_time(), "updated_at": get_time(), "class": type(obj).__name__}

        logger.info(type(obj).__name__)
        if type(obj) is EnterEvent:
            logger.info("insert or update player status")
            self.insert_or_update_playerstatus(game_id, obj)
        return self.raceevent_db.insert(values)

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
        #res = self.playerstatus_db.db.find(query, sort=[( 'bestLap', ASCENDING )])
        res = self.playerstatus_db.db.find(query)
        return res and [_convert(x, PlayerStatus) for x in res]

    def insert_or_update_playerstatus(self, game_id:str, obj: EnterEvent) -> bool:
        playerStatus = PlayerStatus(
            game_id = obj.game_id,
            user_id = obj.user_id,
            user_name = obj.user_name,
            laps_completed = 0,
            total_points = 0,
            best_lap = ""
        )

        id, playerStatusOld = self.find_playerstatus(game_id, obj.user_id)
        if playerStatusOld:
            'reset player information'
            self.update_playerstatus(id, playerStatus)
        else:
            self.insert_playerstatus(playerStatus)
        return True

    def insert_playerstatus(self, obj: PlayerStatus) -> str:
        logger.info("create playerstatus")
        values = {**obj.dict(), "created_at": get_time(), "updated_at": get_time(), "class": type(obj).__name__}
        return self.playerstatus_db.insert(values)

    def update_playerstatus(self, id_: str, obj: PlayerStatus) -> bool:
        logger.info("update playerstatus")
        values = {**obj.dict(), "updated_at": get_time()}
        return self.playerstatus_db.update(id_, values)

    def delete_playerstatus(self, id_: str) -> bool:
        return self.playerstatus_db.delete(id_)

    def get_playerstatus(self, id_: str) -> Optional[PlayerStatus]:
        res = self.playerstatus_db.get(id_)
        return res and _convert(res, PlayerStatus)

    def find_playerstatus(self, game_id:str, user_id: str) -> Optional[PlayerStatus]:
        query = {"game_id":game_id, "user_id":user_id}
        res = self.playerstatus_db.find_one(query)
        logger.info("find playerstatus")
        logger.info(res)
        if res:
            return res['_id'], _convert(res, PlayerStatus)
        return None, None

    def list_playerstati(self, game_id:str) -> List[PlayerStatus]:
        query = {"game_id":game_id}
        res = self.playerstatus_db.find(query)
        return res and [_convert(x, PlayerStatus) for x in res]

    def insert_game(self, obj: Game) -> str:
        values = {**obj.dict(), "created_at": get_time(), "updated_at": get_time(), "class": type(obj).__name__}
        return self.playerstatus_db.insert(values)


class PyMongoClient:
    """Low-Level DB Client for pymongo (synchronous)"""

    def __init__(self, db):
        self.db = db

    def insert(self, obj: dict) -> str:
        res = self.db.insert_one({"_id": uuid.uuid4(), **obj})
        return str(res.inserted_id)

    def get(self, id_: str) -> Optional[dict]:
        return self.db.find_one({"_id": uuid.UUID(id_)})

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
        res = self.db.find(query)
        if res is not None:
            return [res['_id'] for x in res]

    def find_and_get(self, query:dict) -> Optional[List[T]]:
        res = self.db.find(query)
        if res is not None:
            return [_convert(x, self.cls) for x in res]

    def find_one(self, query:dict) -> Optional[str]:
        res = self.db.find_one(query)
        if res is not None:
            return res['_id']

    def find_one_and_get(self, query:dict) -> Optional[T]:
        res = self.db.find(query)
        if res is not None:
            return _convert(res, self.cls)


# Singleton instance
def create_db_client():
    mongo_database_url = settings.database_url
    mongo_client = MongoClient(mongo_database_url)
    return DbClient(mongo_client)


db_client = create_db_client()
