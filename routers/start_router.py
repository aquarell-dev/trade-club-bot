from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from enums import Text
from markups.keyboards import start_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        Text.WELCOME,
        reply_markup=start_keyboard
    )
