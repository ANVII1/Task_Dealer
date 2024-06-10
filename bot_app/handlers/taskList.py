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

class TaskCallbackActions(str,Enum):
    TakeToSelf = "TakeToSelf"
    SendOnTest = "SendOnTest"
    ShowEntry = "ShowEntry"
    Close  = "Close"

class TaskCallback(CallbackData,prefix="c_tsk"):    
    TaskID : str
    Action : TaskCallbackActions

# show my tasks
    
@router.callback_query(MainMenuCallback.filter(F.Navigation == MainMenuActions.myTasks))
async def MyTasksList(callback: CallbackQuery, state : FSMContext):
    
    user = UsersCollection.get_by_tgid(callback.from_user.id)

    user_tasks = TaskCollection.getUserTasks(callback.from_user.id)

    kb = InlineKeyboardBuilder()

    if user.adresation == AdresationGroups.Analysts and user.adresation == AdresationGroups.MasterAnalysts: 
        use_button_text = "Закрыть" 
        use_button_action = TaskCallbackActions.Close 

    else:
        use_button_text = "На тестирование" 
        use_button_action = TaskCallbackActions.SendOnTest 

    kb.row(InlineKeyboardButton(text="[<] Назад", callback_data=MainMenuCallback(Navigation=MainMenuActions.start)))

    for user_task in user_tasks:
        kb.row(
            InlineKeyboardButton(text=user_task.name, callback_data=TaskCallback(TaskID=user_task._id,Action=TaskCallbackActions.ShowEntry)),
            InlineKeyboardButton(text=use_button_text, callback_data=TaskCallback(TaskID=user_task._id,Action=use_button_action))
            )
    
    await callback.bot.send_message(callback.from_user.id, text="Список ваших задач",reply_markup=kb.as_markup())

    
@router.callback_query(MainMenuCallback.filter(F.Navigation == MainMenuActions.urgentTasks))
async def FreeUgrentTasksList(callback: CallbackQuery, state : FSMContext):
    
    user = UsersCollection.get_by_tgid(callback.from_user.id)

    urgent_tasks = TaskCollection.getFreeUgrentTasks(user.adresation)

    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="[<] Назад", callback_data=MainMenuCallback(Navigation=MainMenuActions.start)))

    for _task in urgent_tasks:
        kb.row(
            InlineKeyboardButton(text=_task.name, callback_data=TaskCallback(TaskID=_task._id,Action=TaskCallbackActions.ShowEntry)),
            InlineKeyboardButton(text="Забрать", callback_data=TaskCallback(TaskID=_task._id,Action=TaskCallbackActions.TakeToSelf))
            )
    
    await callback.bot.send_message(callback.from_user.id,text="Список срочных задач:",reply_markup=kb.as_markup())
    

@router.callback_query(MainMenuCallback.filter(F.Navigation == MainMenuActions.sprintTasks))
async def FreeSprintTasksList(callback: CallbackQuery, state : FSMContext):
    
    user = UsersCollection.get_by_tgid(callback.from_user.id)

    urgent_tasks = TaskCollection.getFreeSprintTasks(user.adresation)

    kb = InlineKeyboardBuilder() 

    kb.row(InlineKeyboardButton(text="[<] Назад", callback_data=MainMenuCallback(Navigation=MainMenuActions.start)))

    for _task in urgent_tasks:
        kb.row(
            InlineKeyboardButton(text=_task.name, callback_data=TaskCallback(TaskID=_task._id,Action=TaskCallbackActions.ShowEntry)),
            InlineKeyboardButton(text="Забрать", callback_data=TaskCallback(TaskID=_task._id,Action=TaskCallbackActions.TakeToSelf))
            )
    
    await callback.bot.send_message(callback.from_user.id,text="Список срочных задач:",reply_markup=kb.as_markup())

@router.callback_query(MainMenuCallback.filter(F.Action == TaskCallbackActions.SendOnTest))
async def SendTaskOnTest(callback: CallbackQuery, state : FSMContext):
    callback_data = TaskCallback.unpack(callback.data)
    TaskCollection.sendTaskOnTest(callback_data.TaskID)
    await callback.bot.send_message(callback.from_user.id,"Задача отправлена на тестрование")

@router.callback_query(MainMenuCallback.filter(F.Action == TaskCallbackActions.Close))
async def CloseTask(callback: CallbackQuery, state : FSMContext):
    callback_data = TaskCallback.unpack(callback.data)
    TaskCollection.closeTask(callback_data.TaskID)
    await callback.bot.send_message(callback.from_user.id,"Задача закрыта")

@router.callback_query(MainMenuCallback.filter(F.Action == TaskCallbackActions.ShowEntry))
async def ShowTaskEntry(callback: CallbackQuery, state : FSMContext):
    callback_data = TaskCallback.unpack(callback.data)
    selected_task = TaskCollection.getCurrntTask(callback_data.TaskID)

    text = "Название: " + selected_task.name + "\nАвтор: " + selected_task.author + "\nОписание: " + selected_task.author 

    await callback.bot.send_message(callback.from_user.id,text) 

@router.callback_query(MainMenuCallback.filter(F.Action == TaskCallbackActions.TakeToSelf))
async def getTaskOnExecution(callback: CallbackQuery, state : FSMContext):
    callback_data = TaskCallback.unpack(callback.data)
    TaskCollection.getTaskOnExecute(callback_data.TaskID,callback.from_user.id)

    await callback.bot.send_message(callback.from_user.id, "Вы взяли задачу на исполнение")