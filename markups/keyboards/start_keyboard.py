from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from enums import Button

keyboard = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text=Button.JOIN_TEAM)
    ]],
    resize_keyboard=True,
    input_field_placeholder='Попасть в команду',
    one_time_keyboard=True
)
