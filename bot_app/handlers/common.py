from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from modules.logging import logger as l
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from modules.data import UsersCollection

router = Router()
   
log_dir = "Handlers-common "

# User = UsersCollection.get_by_tgid(msg.from_user.id)

@router.message()
async def message_handler(msg: Message):
    l.inf(log_dir + "main menu message")

    User = UsersCollection.get_by_tgid(msg.from_user.id)
    if User == None:
        await msg.answer("Обратитесь в тех поддержку")
        return

    
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text="Мои текущие задачи",callback_data="mycurrent"))
    
    kb.row(
        InlineKeyboardButton(text="Мои созданные задачи",callback_data="mycreated"))
    
    kb.row(
        InlineKeyboardButton(text="Общие задачи",callback_data="common"))
    
    kb.row(
        InlineKeyboardButton(text="Спринт",callback_data="sprint"))
    

    await msg.answer('Главное меню',reply_markup=kb.as_markup())

