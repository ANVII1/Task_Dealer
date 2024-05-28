from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import Message
from enums.aiogram_states import Registration
from enums.simple_enum import adresations

router = Router()
   
log_dir = "Handlers-registration "


@router.message()
async def message_handler(msg: Message, state : FSMContext):
    await state.set_state(Registration.name)
    await msg.answer("Ввредите имя нового сотрудника")




@router.message(Registration.name)
async def message_handler(msg: Message, state : FSMContext):
    await state.set_state(Registration.adresations)
    
    # check name right 
    
    await state.set_data({"name":msg.text})
    data = await state.get_data()
    name = data["name"]


     

    await msg.answer("Выберите группы адресации для сотрудника {0}".format(name))



@router.message(Registration.adresations)
async def message_handler(msg: Message, state : FSMContext):
    await state.set_state(Registration.name)
    
    
    
    await state.set_data({"name":msg.text})
    data = await state.get_data()
    name = data["name"]

    text = "Введите Telegram id Нового сотрудника \n Telegram id можно узнать в боте **getmyid_bot**"

    await msg.answer(text)



@router.message(Registration.id)
async def message_handler(msg: Message, state : FSMContext):
    await state.set_state(Registration.name)
    
    
    
    text = "Новый сотрудник успешно зарегистрирован:\n\
        **Имя:** {0}\
        **Группы адресации:** {1}\
        **TelegramID:** {2}"

    await msg.answer(text)