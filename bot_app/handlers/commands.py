from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from modules.logging import logger as l
from modules.data import UsersCollection
import datetime as dt
from enums.simple_enum import adresations

log_dir = "handlers-commands "

router = Router()

@router.message(Command("echo"))
async def echo(msg: Message):
       l.inf(log_dir + "echo")
       await msg.answer("echo command is touched")

@router.message(Command("set"))
async def database_test(msg: Message):
       """
       isert me in database
       """
       l.inf(log_dir + "inserted in database")
       UsersCollection.new(msg.from_user.id,"Anvie",adresations.Developers)
       await msg.answer("you have been added to database")

@router.message(Command("get"))
async def database_test(msg: Message):
       """
       get me from database
       """
       l.inf(log_dir + "user getted from data base")
       userData = UsersCollection.get_by_tgid(msg.from_user.id)
       await msg.answer(str(userData))
       