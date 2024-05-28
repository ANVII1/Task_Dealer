from pymongo import MongoClient
import utils.envvars as env
from modules.logging import logger as l
import datetime as dt

log_dir = "modules-data ::: "


DB_CLIENT:MongoClient = MongoClient(f'mongodb://{env.DB_HOST}:{env.DB_PORT}')
db = DB_CLIENT.database

#usersCollection = db.users

#Region Objects from database
class db_obj():
    object : dict
    def __init__(self,data:dict) -> None:
        self.object = data

    def __getattr__(self, name: str):
        return object[name]
# ////////////////////////////////

class User(db_obj):
    def __init__(self,data:dict) -> None:
        super().__init__(data)
    pass

class Task(db_obj):
    def __init__(self,data:dict) -> None:
        super().__init__(data)
#endreion
    
    
#region Collections from database
class UsersCollection:

    @classmethod
    def get_to_notify(self):
        return db.users.find({"notify": { "$eq" : True } })
    
    @classmethod
    def get_by_adresation(self,adresation):
        return db.users.find({"adresation": { "$eq" : adresation } })
    

    @classmethod
    def get_by_tgid(self, telegramID:str)-> User:
        return list( db.users.find_one( {"telegramID": {"$eq" : telegramID}} ) ) 


    @classmethod
    def new(self, telegramID:int ,name:str, adresations: str | list[str]) -> bool:
        data_ : dict = {
            "telegramID" : telegramID,
            "name" : name,
            
            "notify" : True,
            "adresations" : adresations

        }
        db.users.insert_one(data_)          


#endregion