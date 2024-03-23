from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from enums.callbacks import Callback
from settings import get_env

env = get_env()

markup = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
            text='Регистрация',
            url=env.REGISTER_URL
        ),
        InlineKeyboardButton(
            text='Прислать UID',
            callback_data=Callback.CHECK_UID
        ),
        InlineKeyboardButton(
            text='Я не ваш партнер',
            callback_data=Callback.ALREADY_AFFILIATE
        )
    ]]
)

builder = InlineKeyboardBuilder(markup=markup.inline_keyboard)

builder.adjust(1, repeat=True)

keyboard = builder.as_markup()
