from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram import F
from enum import Enum
from callbacks.mainMenu import MainMenuActions, MainMenuCallback 
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from modules.data import UsersCollection, TaskCollection, Task
from handlers.taskList import TaskCallbackActions, TaskCallback

router = Router()
   
log_dir = "Handlers-registration "

sprint_tasks : list[Task] = []

class SprintCallbackActions(str,Enum):
    CloseSprint = "CloseSprint"
    StartSprint = "StartSprint"
    TakeToSprint = "TakeToSprint"
    DeclineFromSprint = "DeclineFromSprint"

class SprintTaskCallback(CallbackData,prefix="c_tsk"):    
    TaskID : str
    Action : SprintCallbackActions

# show my tasks
    
@router.callback_query(MainMenuCallback.filter(F.Navigation == MainMenuActions.sprintMenu))
async def SprintMenu(callback: CallbackQuery, state : FSMContext):
    kb = InlineKeyboardBuilder()

    if TaskCollection.isSprintRunning():
        kb.row(
            InlineKeyboardButton(text="Да",callback_data=SprintTaskCallback(Action=SprintCallbackActions.CloseSprint).pack()),
            InlineKeyboardButton(text="Нет",callback_data=MainMenuCallback(Navigation=MainMenuActions.start).pack())
        )
        await callback.bot.send_message(callback.from_user.id,"Зкончить текущий спринт?", reply_markup=kb.as_markup())
        return
    
    kb.row(
        InlineKeyboardButton(text="Назад",callback_data=MainMenuCallback(Navigation=MainMenuActions.start).pack())
    )

    if len(sprint_tasks):
        kb.row(
            InlineKeyboardButton(text="Начать спринт",callback_data=SprintTaskCallback(Action=SprintCallbackActions.StartSprint).pack())
        )

    backlog_tasks_list = TaskCollection.getBacklogTasks()
    for _task in backlog_tasks_list:

        _second_button_text = "Убрать" if _task._id in sprint_tasks else "Добавить" 
        _second_button_callback = SprintTaskCallback(Action= SprintCallbackActions.DeclineFromSprint if _task._id in sprint_tasks else SprintCallbackActions.TakeToSprint)

        kb.row(
            InlineKeyboardButton(text=_task.name,callback_data=TaskCallback(Action=TaskCallbackActions.ShowEntry).pack()),
            InlineKeyboardButton(text=_second_button_text,callback_data=_second_button_callback.pack())
        )

    await callback.bot.send_message(callback.from_user.id,"Задачи спринта", reply_markup=kb.as_markup())

@router.callback_query(SprintTaskCallback.filter(F.Action == SprintCallbackActions.TakeToSprint))
async def TakeTaskInSprint(callback: CallbackQuery, state : FSMContext):
    callback_data = SprintTaskCallback.unpack(callback)
    sprint_tasks.append(callback_data.TaskID) 
    await SprintMenu(callback,state)
    
    

@router.callback_query(SprintTaskCallback.filter(F.Action == SprintCallbackActions.DeclineFromSprint))
async def DeclineTaskFromSprint(callback: CallbackQuery, state : FSMContext):
    callback_data = SprintTaskCallback.unpack(callback)
    sprint_tasks.remove(callback_data.TaskID) 
    await SprintMenu(callback,state)


@router.callback_query(SprintTaskCallback.filter(F.Action == SprintCallbackActions.StartSprint))
async def StartSprint(callback: CallbackQuery, state : FSMContext):
    TaskCollection.startSprint(sprint_tasks)
    users = UsersCollection.get_all_users()
    for user in users:
        await callback.bot.send_message(user.telegramID,"Начат новый спринт")

@router.callback_query(SprintTaskCallback.filter(F.Action == SprintCallbackActions.CloseSprint))
async def CloseSprint(callback: CallbackQuery, state : FSMContext):
    TaskCollection.closeSprint()
    users = UsersCollection.get_all_users()
    for user in users:
        await callback.bot.send_message(user.telegramID,"Cпринт окончен!")

    