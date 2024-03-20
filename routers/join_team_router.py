import aiogram.exceptions
import aiohttp
from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from affiliate.exceptions import AffiliateException
from enums.callbacks import Callback
from exchange import Bybit
from markups.keyboards import join_team_keyboard
from redis_client import client
from settings import get_env
from states import CheckUserIdState

router = Router()

env = get_env()
bybit = Bybit()


@router.callback_query(F.data == Callback.ALREADY_AFFILIATE)
async def already_affiliate_handler(callback: CallbackQuery, bot: Bot) -> None:
    already_affiliate = await client.get('already_affiliate')

    await bot.send_photo(
        callback.from_user.id,
        photo=await client.get('change_affiliation_file'),
        caption=already_affiliate,
        reply_markup=join_team_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == Callback.CHECK_UID)
async def check_user_id_start_handler(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    check_uid = await client.get('check_uid')

    await bot.send_photo(
        callback.from_user.id,
        photo=await client.get('find_uid_file'),
        caption=check_uid
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
        await bot.send_message(tg_user_id, await e.get_message())
        return
    except aiohttp.ClientError as e:
        await bot.send_message(tg_user_id, await client.get('request_uid_error'))
        return

    try:
        invite_link = await bot.create_chat_invite_link(
            chat_id=env.GROUP_ID,
            member_limit=1
        )
    except aiogram.exceptions.AiogramError:
        await bot.send_message(tg_user_id, text='Ошибка, не удалось сгенерировать ссылку.')
        return

    await bot.send_message(tg_user_id, text=f'Отлично, вот ваша ссылка: {invite_link.invite_link}')


@router.message(CheckUserIdState.enter_uid)
async def enter_user_id_not_valid_user_id(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, await client.get('invalid_uid_format'))
