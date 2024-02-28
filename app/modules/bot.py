from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram import types
import os

class bot:
    bot: Bot

    @classmethod
    def init(self) -> None:
       bot = Bot(token=os.environ['MY_TG_TOKEN'], parse_mode=ParseMode.HTML)

    @classmethod
    def send_message(self,user_id:int,message:str,reply_markup = None):
        self.bot.send_message(user_id,text=message,reply_markup=reply_markup)