from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from markups.keyboards import join_team_keyboard
from redis_client import client

router = Router(name=__name__)


@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot) -> None:
    await bot.send_video(
        message.from_user.id,
        video=await client.get('welcome_video_file'),
        caption=await client.get('welcome'),
        reply_markup=join_team_keyboard
    )
