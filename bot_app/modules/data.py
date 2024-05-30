from pymongo import MongoClient,CursorType
import utils.envvars as env
from modules.logging import logger as l
import datetime as dt
from enums.simple_enum import AdresationGroups, TaskStates

log_dir = "modules-data ::: "


DB_CLIENT:MongoClient = MongoClient(f'mongodb://{env.DB_HOST}:{env.DB_PORT}')
db = DB_CLIENT.database

#usersCollection = db.users

#Region Objects from database
class db_obj():    
    def __init__(self,_id) -> None:
        self._id = _id

# ////////////////////////////////

class User(db_obj):
    def __init__(self,data:CursorType) -> None:
        if data is None:
            return None

        super().__init__(data["_id"])
        self.telegramID = str(data["telegramID"])
        self.name : str = data["name"]        
        self.adresation : AdresationGroups = data["adresation"]

    def __repr__(self) -> str:
        return self.name + " : " + self.telegramID
        

class Task(db_obj):
    def __init__(self,data:CursorType) -> None:
        if data is None:
            return None

        super().__init__(data["_id"])
        self.name : str = data["name"]
        self.description : str = data["description"]
        self.adresation : AdresationGroups = data["adresation"]
        self.status = data["status"]
        self.author : str = data["author"]
        self.executor : str = data["executor"]

    
    def __repr__(self) -> str:
        return self.name
        

#endreion
    
    
#region Collections from database
class UsersCollection:
    
    @classmethod
    def get_by_adresation(self,adresation) -> list[User]:
        
        cursor = db.users.find({"adresation": { "$eq" : adresation } })

        users : list[User] = [] 

        if cursor is None:
            return users

        for cUser in cursor:
            users.append(User(cUser))

        return users
    

    @classmethod
    def get_by_tgid(self, telegramID:str)-> User:
        cursor = db.users.find_one( {"telegramID": {"$eq" : telegramID}} )
        
        if cursor is None:
            return None

        return User(cursor) 


    @classmethod
    def new(self, telegramID : int ,name : str, adresation : AdresationGroups):
        data_ : dict = {
            "telegramID" : telegramID,
            "name" : name,
            "adresation" : adresation

        }
        db.users.insert_one(data_)          


class TaskCollection:
    @classmethod
    def getFreeSprintTasks(self,adresation : AdresationGroups):
        db.tasks.find(
            {
                "adresation" : {
                    "$eq" : adresation
                },
                "state": {
                    "$eq" : TaskStates.Sprintfree
                }
            }            
        )
    
    @classmethod
    def getFreeUgrentTasks(self,adresation : AdresationGroups):
        db.tasks.find(
                {
                    "adresation" : {
                        "$eq" : adresation
                    },
                    "state": {
                        "$eq" : TaskStates.Urgentfree
                    }
                }            
            )

    @classmethod
    def getUserTasks(self,telegramID : str):
        return db.tasks.find({"executor" : { "$eq" : telegramID}})

    @classmethod
    def createUrgentTask(self,name : str, description : str, AuthorTelegramID : str, adresation : AdresationGroups):
        self._createBaseTask(name,description,AuthorTelegramID,adresation,True)

    @classmethod
    def createSprintTask(self,name : str, description : str, AuthorTelegramID : str, adresation : AdresationGroups):
        self._createBaseTask(name,description,AuthorTelegramID,adresation)

    @classmethod
    def _createBaseTask(self,name : str, description : str, AuthorTelegramID : str, adresation : AdresationGroups,urgent=False):
        author = db.users.find_one({"telegramID":AuthorTelegramID})
        typeOfTask = TaskStates.inBacklog if not urgent else TaskStates.Urgentfree
        db.tasks.insert_one(
                {
                    "name":name,
                    "description": description,
                    "adresation" : adresation,    
                    "executor"  : None,
                    "author"  : author["_id"],
                    "state" : typeOfTask
                }
            )

    @classmethod
    def closeTask(self,taskID:str):
        ...

    @classmethod
    def startSprint(self,selectedTasks:list[Task]):
        for task in selectedTasks:
            db.tasks.update_one(
                {
                    "_id":task["_id"]
                },
                {
                    "$set": {
                        "state" : TaskStates.Sprintfree
                    }
                }
            )    
        

    @classmethod
    def closeSprint(self):
        """
        all tasks wich is not done, move to backlog
        """
        ...

    
    @classmethod
    def closeTask(self,taskID:str):
        """
        all tasks wich is not done, move to backlog
        """
        UnclosedTasks = {

        }

    @classmethod
    def sendTaskOnTest(self,taskID:str):
        task = db.tasks.find_one({"_id":taskID})
        executor = db.users.find_one({"_id":task["executor"]})
        author = db.users.find_one({"_id":task["author"]}) 

        db.tasks.update_one(
                {
                    "_id":taskID
                },
                {
                    "$set": {
                        "name":task["name"] + " (Тест)",
                        "description": "Протестировать: \n" + task["description"],
                        "adresation" : author["adresation"],    
                        "executor"  : author["_id"],
                        "author"  : executor["_id"],
                        "state" : TaskStates.UrgentinProgress
                    }
                }
            )

#endregion