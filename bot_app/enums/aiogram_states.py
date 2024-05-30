from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    name = State()
    adresations = State()
    id = State()

class TaskCreation(StatesGroup):
    name = State()
    description = State()