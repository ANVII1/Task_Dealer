from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import Message
from enums.aiogram_states import TaskCreation
from enums.simple_enum import AdresationGroups, TaskStates
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram import F
from aiogram import Bot
from enum import Enum
from callbacks.mainMenu import MainMenuActions, MainMenuCallback 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.enums.parse_mode import ParseMode 
from modules.data import UsersCollection, TaskCollection
from utils.morpher import adresationGroupToName
from handlers.common import message_handler

router = Router()
   
log_dir = "Handlers-registration "

class taskCreationCallBack(CallbackData,prefix="tsk_crt"):
    taskType : TaskStates
    adresation : AdresationGroups

@router.callback_query(MainMenuCallback.filter(F.Navigation == MainMenuActions.createTask))
async def CreateTask1(callback:CallbackQuery):

    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text="Спринтовая", callback_data=taskCreationCallBack(taskType=TaskStates.inBacklog))
    )

    kb.row(
        InlineKeyboardButton(text="Срочная", callback_data=taskCreationCallBack(taskType=TaskStates.Urgentfree))
    )

    await callback.bot.send_message(callback.from_user.id,text="Укажите тип задачи:", reply_markup=kb.as_markup())


@router.callback_query(taskCreationCallBack.filter(F.adresation == None))
async def CreateTask2(callback:CallbackQuery,  state : FSMContext):
    data = taskCreationCallBack.unpack(callback.data)
    
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text="Разработчик",
            callback_data=taskCreationCallBack(adresation=AdresationGroups.Developers,taskType=data.taskType).pack()))
    
    kb.row(
        InlineKeyboardButton(text="Системный Администратор",
            callback_data=taskCreationCallBack(adresation=AdresationGroups.SysAdmins,taskType=data.taskType).pack()))
    
    kb.row(
        InlineKeyboardButton(text="Аналитик",
            callback_data=taskCreationCallBack(adresation=AdresationGroups.Analysts,taskType=data.taskType).pack()))
    
    kb.row(
        InlineKeyboardButton(text="Ведущий аналитик",
            callback_data=taskCreationCallBack(adresation=AdresationGroups.MasterAnalysts,taskType=data.taskType).pack()))

    await callback.bot.send_message(callback.from_user.id,text="Выберите группу адресации для задачи", reply_markup=kb.as_markup())


@router.callback_query(taskCreationCallBack.filter((F.adresation != None) and (F.taskType != None)))
async def CreateTask3(callback:CallbackQuery,  state : FSMContext):
    data = taskCreationCallBack.unpack(callback.data)
    
    await state.set_state(TaskCreation.name)

    await state.set_data(
            {
                "Adresation":data.adresation,
                "type" : data.taskType
            }
        )

    await callback.bot.send_message(callback.from_user.id,text="Выберите наименование задачи")


@router.callback_query(TaskCreation.name)
async def CreateTask4(msg:Message,  state : FSMContext):
    
    await state.set_state(TaskCreation.name)

    await state.set_data(
            {
                "name":msg.text
            }
        )

    await msg.answer(text="Введите описание для задачи или ссылку на ТЗ")


@router.callback_query(TaskCreation.description)
async def CreateTask5(msg:Message,  state : FSMContext):

    data = state.get_data()

    taskType = data["taskType"]
    adresation = data["adresation"]
    name = data["name"]
    description = msg.text

    if taskType == TaskStates.inBacklog:
        TaskCollection.createSprintTask(name,description,msg.from_user.id,adresation)
    else:
        TaskCollection.createUrgentTask(name,description,msg.from_user.id,adresation)

    await msg.answer(text="Задача успешно создана")
    await message_handler(msg)