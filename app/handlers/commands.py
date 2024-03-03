from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import logging as l

log_dir = "Handlers ::: commands ::: "

router = Router()

@router.message(Command("echo"))
async def echo(msg: Message):
       await msg.answer("echo command is touched")
       l.info(log_dir + "random message")