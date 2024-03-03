from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import logging as l

log_dir = "handlers ::: commands ::: "

router = Router()

@router.message(Command("echo"))
async def echo(msg: Message):
       l.info(log_dir + "echo")
       await msg.answer("echo command is touched")
       