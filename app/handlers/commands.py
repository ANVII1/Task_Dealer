from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import logging as l
from pymongo import MongoClient
import utils.envvars as env

log_dir = "handlers ::: commands ::: "

router = Router()

@router.message(Command("echo"))
async def echo(msg: Message):
       l.info(log_dir + "echo")
       await msg.answer("echo command is touched")

@router.message(Command("database_test"))
async def echo(msg: Message):
       l.info(log_dir + "database tested")
       try:
              db_client =  MongoClient(f'mongodb://{env.DB_HOST}:{env.DB_PORT}')
              db = db_client.my_database
              collection = db.new_collection
              collection.insert_one({"name":"main_", "text":"hello world"})  
              
              await msg.answer((collection.find_one({"name":"main_"}))["text"])
       except Exception as e:
              l.exception(log_dir + "database ::: " + str(e))