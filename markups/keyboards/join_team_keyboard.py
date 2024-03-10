from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from enums import Button
from enums.callbacks import Callback
from settings import get_env

env = get_env()

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
            text=Button.REGISTER,
            url=env.REGISTER_URL
        ),
        InlineKeyboardButton(
            text=Button.CHECK_UID,
            callback_data=Callback.CHECK_UID
        ),
        InlineKeyboardButton(
            text=Button.ALREADY_AFFILIATE,
            callback_data=Callback.ALREADY_AFFILIATE
        )
    ]]
)
