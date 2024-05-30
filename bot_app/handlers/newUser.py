from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import Message
from enums.aiogram_states import Registration
from enums.simple_enum import AdresationGroups
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram import F
from aiogram import Bot
from enum import Enum
from callbacks.mainMenu import MainMenuActions, MainMenuCallback 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.enums.parse_mode import ParseMode 
from modules.data import UsersCollection
from utils.morpher import adresationGroupToName


router = Router()
   
log_dir = "Handlers-registration "

class SettingAdresationCallback(CallbackData,prefix="c_adr"):    
    Telegramid : str
    Name : str
    Adresation: AdresationGroups
    
@router.callback_query(MainMenuCallback.filter(F.Navigation == MainMenuActions.createUser))
async def reg_entery_point(callback: CallbackQuery, state : FSMContext):
    await state.set_state(Registration.id)

    await callback.bot.send_message(callback.from_user.id, text="Введите Telegram id Нового сотрудника")
   

@router.message(Registration.id)
async def reg_id(msg: Message, state : FSMContext):
    
    await state.set_state(Registration.name)
    await state.set_data({"tg_id" : msg.text})

    await msg.answer(text="Введите имя нового сотрудника")


@router.message(Registration.name)
async def reg_name(msg: Message, state : FSMContext):
    
    data = await state.get_data()
    name = msg.text
    id = data["tg_id"]

    KB = InlineKeyboardBuilder()

    KB.row(
        InlineKeyboardButton(text="Разработчик",
            callback_data=SettingAdresationCallback(Adresation=AdresationGroups.Developers,Name=name,Telegramid=id).pack()))
    
    KB.row(
        InlineKeyboardButton(text="Системный Администратор",
            callback_data=SettingAdresationCallback(Adresation=AdresationGroups.SysAdmins,Name=name,Telegramid=id).pack()))
    
    KB.row(
        InlineKeyboardButton(text="Аналитик",
            callback_data=SettingAdresationCallback(Adresation=AdresationGroups.Analysts,Name=name,Telegramid=id).pack()))
    
    KB.row(
        InlineKeyboardButton(text="Ведущий аналитик",
            callback_data=SettingAdresationCallback(Adresation=AdresationGroups.MasterAnalysts,Name=name,Telegramid=id).pack()))


    await msg.answer("Выберите группы адресации для сотрудника {0}".format(name),reply_markup=KB.as_markup())


@router.callback_query(SettingAdresationCallback.filter(F.Adresation != ""))
async def reg_adresation(callback: CallbackQuery, state : FSMContext):
    await state.set_state(Registration.id)

    data = SettingAdresationCallback.unpack(callback.data)
    
    UsersCollection.new(data.Telegramid,data.Name,data.Adresation)

    text = "Новый сотрудник успешно зарегистрирован:\nИмя: " + data.Name + "\nГруппа адресации: " + adresationGroupToName(data.Adresation) + "\nTelegramID: " + data.Telegramid 

    await callback.bot.send_message(callback.from_user.id, text=text,parse_mode=ParseMode.MARKDOWN_V2)
