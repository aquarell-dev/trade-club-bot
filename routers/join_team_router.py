import aiogram.exceptions
import aiohttp
from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from affiliate.exceptions import AffiliateException
from enums import Button, Text
from enums.callbacks import Callback
from exchange import Bybit
from markups.keyboards import join_team_keyboard
from settings import get_env
from states import CheckUserIdState

router = Router()

env = get_env()
bybit = Bybit()


@router.message(F.text == Button.JOIN_TEAM)
async def join_team_handler(message: Message, bot: Bot) -> None:
    await bot.send_message(
        chat_id=message.from_user.id,
        text=Text.JOIN_TEAM,
        reply_markup=join_team_keyboard
    )


@router.callback_query(F.data == Callback.ALREADY_AFFILIATE)
async def register_user_handler(callback: CallbackQuery, bot: Bot) -> None:
    await bot.send_message(
        callback.from_user.id,
        text=Text.ALREADY_AFFILIATE,
        reply_markup=join_team_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == Callback.CHECK_UID)
async def register_user_handler(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.send_message(
        callback.from_user.id,
        text=Text.CHECK_UID,
    )
    await callback.answer()
    await state.set_state(CheckUserIdState.enter_uid)


@router.message(CheckUserIdState.enter_uid, F.text.regexp(r"^(\d+)$"))
async def enter_user_id(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()

    tg_user_id = message.from_user.id

    try:
        affiliate = await bybit.get_affiliate(message.text)
    except AffiliateException as e:
        await bot.send_message(tg_user_id, e.get_message())
        return
    except aiohttp.ClientError as e:
        await bot.send_message(tg_user_id, Text.REQUEST_UID_ERROR)
        return

    try:
        invite_link = await bot.create_chat_invite_link(
            chat_id=env.GROUP_ID,
            member_limit=1
        )
    except aiogram.exceptions.AiogramError:
        await bot.send_message(tg_user_id, text=Text.UNSUCCESSFUL_CHECK)
        return

    await bot.send_message(tg_user_id, text=Text.SUCCESSFUL_CHECK.format(invite_link.invite_link))


@router.message(CheckUserIdState.enter_uid)
async def enter_user_id_not_valid_user_id(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, Text.INVALID_UID_FORMAT)
