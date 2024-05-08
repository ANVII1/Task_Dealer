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
        return db.users.find({"notify": { "$eq": True } })
    
    @classmethod
    def get_by_adresation(self,adresation):
        return db.users.find({"adresation": { "$eq": adresation } })
    

    @classmethod
    def get_by_tgid(self, telegramID:str)-> User:
        return list( db.users.find_one( {"telegramID":telegramID} ) ) 


    @classmethod
    def new(self, telegramID:int ,name:str, adresations: str | list[str]) -> bool:
        data_ : dict = {
            "telegramID" : telegramID,
            "name" : name,
            
            "notify" : True,
            "adresations" : adresations

        }
        db.users.insert_one(data_)          


class TaskCollection:

    @classmethod
    def get_for_execute(self) -> list[dict]:
        """
        return's a list of tasks where exec_time equal or less than current date-time        
        """
        query = { "exec_time": { "$lte": dt.datetime.now() } }
        tasks_count = db.tasks.count_documents(query)
        if tasks_count == 0:
            return None        
        return db.tasks.find(query)
        
                 

    @classmethod
    def update_exec_time(task:str,new_time:dt.datetime):
        db.tasks.update_one({"_id":task["_id"]},{ "$set":{"exec_time":new_time}})

    def remove(task:dict):
        db.tasks.delete_one({"_id":task["_id"]})
    
    @classmethod
    def new(self, func_name:str, next_time:dt.datetime, reglament:dict|None, args:dict[str]|None) -> bool:
        """
        reglament is a dict in format
        {
            "time" : str,

            "weekdays" : array[str]
                or
            "on_date" : str
        }
        if reglament is none thats mean func will execute once
        """
        
        query : dict = {
            "exec_time":next_time,               
            "func_name" : func_name
            }
        
        if reglament is not None:
            query["reglament"] = reglament
        
        if args is not None:
            query["args"] = args
        
        db.tasks.insert_one(query)          

#endregion