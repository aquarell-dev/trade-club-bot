import aiogram.exceptions
import aiohttp
from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from affiliate.exceptions import (
    AffiliateAlreadyExists, InvalidAffiliateException,
    NotEnoughDepositException, NotEnoughTradingVolumeException
)
from enums.callbacks import Callback
from markups.keyboards import join_team_keyboard, start_keyboard
from redis_client import client
from services.affiliate_service import add_affiliate
from settings import get_env
from states import CheckUserIdState

router = Router()

env = get_env()


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


@router.callback_query(F.data == Callback.START)
async def handle_start(callback: CallbackQuery, bot: Bot) -> None:
    await bot.send_video(
        callback.from_user.id,
        video=await client.get('welcome_video_file'),
        caption=await client.get('welcome'),
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

    try:
        await add_affiliate(message.text)
    except InvalidAffiliateException as e:
        await bot.send_photo(
            message.from_user.id,
            photo=await client.get('change_affiliation_file'),
            caption=await e.get_message(),
            reply_markup=start_keyboard
        )
        return
    except (
        NotEnoughDepositException, NotEnoughTradingVolumeException, AffiliateAlreadyExists
    ) as e:
        await bot.send_message(
            message.from_user.id,
            await e.get_message(),
            reply_markup=start_keyboard
        )
        return
    except aiohttp.ClientError as e:
        await bot.send_message(
            message.from_user.id,
            await client.get('request_uid_error'),
            reply_markup=start_keyboard
        )
        return

    try:
        invite_link = await bot.create_chat_invite_link(
            chat_id=env.GROUP_ID,
            member_limit=1
        )
    except aiogram.exceptions.AiogramError:
        await bot.send_message(
            message.from_user.id,
            text='Ошибка, не удалось сгенерировать ссылку.',
            reply_markup=start_keyboard
        )
        return

    await bot.send_message(
        message.from_user.id,
        text=f'Отлично, вот ваша <i>одноразовая</i> ссылка на доступ в Клуб: {invite_link.invite_link}',
        reply_markup=start_keyboard
    )


@router.message(CheckUserIdState.enter_uid)
async def enter_user_id_not_valid_user_id(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, await client.get('invalid_uid_format'))
