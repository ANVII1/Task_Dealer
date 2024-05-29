from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from modules.logging import logger as l
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from modules.data import UsersCollection
from enums.simple_enum import AdresationGroups
from callbacks.mainMenu import MainMenuActions, MainMenuCallback

router = Router()
   
log_dir = "Handlers-common "

# User = UsersCollection.get_by_tgid(msg.from_user.id)

@router.message()
async def message_handler(msg: Message):
    l.inf(log_dir + "main menu message")

    user = UsersCollection.get_by_tgid(msg.from_user.id)
    if user == None:
        await msg.answer("Обратитесь в тех поддержку")
        return

    
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text="Мои текущие задачи",
            callback_data=MainMenuCallback(Navigation=MainMenuActions.myTasks).pack()))
    
    kb.row(
        InlineKeyboardButton(text="Срочные задачи",
            callback_data=MainMenuCallback(Navigation=MainMenuActions.urgentTasks).pack()))
    
    kb.row(
        InlineKeyboardButton(text="задачи спринта",
            callback_data=MainMenuCallback(Navigation=MainMenuActions.sprintTasks).pack()))

    # if (user.adresation == AdresationGroups.Analysts 
    #     or user.adresation == AdresationGroups.MasterAnalysts):
        
    kb.row(
        InlineKeyboardButton(text="Создать задачу",
            callback_data=MainMenuCallback(Navigation=MainMenuActions.createTask).pack()))    

    # if user.adresation == AdresationGroups.MasterAnalysts:        
    kb.row(
        InlineKeyboardButton(text="Управление Спринтом",
            callback_data=MainMenuCallback(Navigation=MainMenuActions.manageSprint).pack()))
    
    # if user.adresation == AdresationGroups.SysAdmins:
    kb.row(
        InlineKeyboardButton(text="Создать пользователя",
            callback_data=MainMenuCallback(Navigation=MainMenuActions.createUser).pack()))   

    await msg.answer('Главное меню',reply_markup=kb.as_markup())

