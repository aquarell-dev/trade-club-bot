from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from enums.callbacks import Callback
from settings import get_env

env = get_env()

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
            text='В начало',
            callback_data=Callback.START
        )
    ]]
)
