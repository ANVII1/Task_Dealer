from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import logging as l

router = Router()
   
log_dir = "Handlers ::: common ::: "

@router.message()
async def message_handler(msg: Message):
    l.info(log_dir + "general message")
    await msg.answer('you say "{0}"'.format(msg.text))