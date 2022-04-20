"""
Module providing uniform access to the database, taking care of generating unique IDs for the elements,
converting them back to their actual data types on retrieval, etc.
"""

from datetime import timedelta
import time
import uuid
from typing import List, Optional

from pymongo import MongoClient, DESCENDING, ASCENDING

from .model import RaceEvent, EnterEvent, StartMotorEvent, BarcodeEvent, PointsAwardedEvent, FinishEvent
from .model_racedisplay import PlayerStatus
from .singletons import settings, logger


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

    def insert_raceevent(self, race_id:str, obj: RaceEvent, sha3_password = None) -> str:
        values = {**obj.dict(), "created_at": get_time(), "updated_at": get_time(), "class": type(obj).__name__, "race": race_id}
        if obj is EnterEvent:
            self.insert_or_update_playerstatus(race_id, obj)
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

    def get_scoreboard(self, race_id:str) -> str:
        query = {"race":race_id}
        #res = self.playerstatus_db.db.find(query, sort=[( 'bestLap', ASCENDING )])
        res = self.playerstatus_db.db.find(query)
        return res and [_convert(x, globals()[x["class"]]) for x in res]

    def insert_or_update_playerstatus(self, race_id:str, obj: EnterEvent) -> bool:
        #construct new player status object
        playerStatus = PlayerStatus(
            uuid = obj.uuid, 
            timestamp = obj.timestamp,
            enterEvent = obj,
            lapsCompleted = 0,
            totalPoints = 0,
            bestLap = None
            )
        result = self.find_playerstatus(race_id, obj.uuid)
        if result:
            self.update_playerstatus(self, result.id, playerStatus)
        else:
            self.insert_playerstatus(self, race_id, playerStatus)
        return True

    def insert_playerstatus(self, race_id:str, obj: PlayerStatus) -> str:
        values = {**obj.dict(), "created_at": get_time(), "updated_at": get_time(), "class": type(obj).__name__, "race": race_id}
        return self.playerstatus_db.insert(values)

    def update_playerstatus(self, id_: str, obj: PlayerStatus) -> bool:
        values = {**raceevent.dict(), "updated_at": get_time()}
        return self.playerstatus_db.update(id_, values)

    def delete_playerstatus(self, id_: str) -> bool:
        return self.playerstatus_db.delete(id_)

    def get_playerstatus(self, id_: str) -> Optional[PlayerStatus]:
        res = self.playerstatus_db.get(id_)
        return res and _convert(res, PlayerStatus)

    def find_playerstatus(self, race_id:str, uuid: uuid) -> Optional[PlayerStatus]:
        query = {"race":race_id, "uuid":uuid}
        res = self.playerstatus_db.find(query)
        return _convert(res, PlayerStatus)

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

    def update(self, id_: str, values: dict) -> bool:
        res = self.db.update_one({"_id": uuid.UUID(id_)}, {"$set": values})
        return res.modified_count == 1

    def delete(self, id_: str) -> bool:
        res = self.db.delete_one({"_id": uuid.UUID(id_)})
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



# Singleton instance
def create_db_client():
    mongo_database_url = settings.database_url
    mongo_client = MongoClient(mongo_database_url)
    return DbClient(mongo_client)


db_client = create_db_client()
