from aiogram.filters.callback_data import CallbackData
from enum import Enum

class MainMenuActions(str,Enum):
    createTask = "createTask"
    createUser = "createUser"
    manageSprint  = "manageSprint"    
    urgentTasks = "urgentTasks"
    sprintTasks = "sprintTasks"
    myTasks = "myTasks"
    start = "start"
    sprintMenu = "sprintMenu"

class MainMenuCallback(CallbackData,prefix="main"):
    Navigation: MainMenuActions
