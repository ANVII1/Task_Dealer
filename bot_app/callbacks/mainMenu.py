from aiogram.filters.callback_data import CallbackData
from enum import Enum

class MainMenuActions(str,Enum):
    createTask = "createTask"
    createUser = "createUser"
    manageSprint  = "manageSprint"    
    urgentTasks = "urgentTasks"
    sprintTasks = "sprintTasks"
    myTasks = "myTasks"

class MainMenuCallback(CallbackData,prefix="main"):
    Navigation: MainMenuActions