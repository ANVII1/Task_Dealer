from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# // -------- Misc (Разное мелкое)
def constructKB(buttons:list) -> InlineKeyboardMarkup:

    KB = InlineKeyboardBuilder()

    for button in buttons:
        KB.row(
            InlineKeyboardButton(
                text=button["text"],
                callback_data=button["callback_data"]
                )
            )

    return KB.as_markup()