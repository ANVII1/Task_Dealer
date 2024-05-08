"""
////
//// to any outer access to scheduler should use funs from this module
////
"""

from modules.scheduler.anvSched import newTask
from modules.scheduler.reglaments import *

"""
High-level wrapped funcs for scheduler to plan tasks
"""

async def CreateMessage(telegramID : int, text : str, time:str ,reglament : dict | None=None):        
    await newTask(sendMessage,time=time,args=(telegramID, text),reglament=reglament)