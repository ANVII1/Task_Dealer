"""
////
//// All schedulable tasks place here as global async func's
////
"""

from modules.telegram import bots
from aiogram import Bot
from utils import keyboards
import datetime as dt
from modules.data import UsersCollection

async def sendMessage(telegramID:int,text:str):
    await bots.get_by_name("DEALER").send_message(telegramID,text=text)