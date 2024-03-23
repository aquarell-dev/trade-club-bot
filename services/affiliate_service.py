from affiliate.exceptions import (
    AffiliateAlreadyExists,
    InvalidAffiliateException,
    NotEnoughDepositException, NotEnoughTradingVolumeException
)
from exchange import Bybit
from redis_client import client
from settings import get_env

bybit = Bybit()
env = get_env()


async def _is_affiliate_already_joined(affiliate_id: str) -> bool:
    affiliates: list[bytes] = await client.lrange('affiliates', 0, -1)  # list of affiliates ids

    for affiliate in affiliates:
        if affiliate.decode('utf-8') == affiliate_id:
            return True

    return False


async def add_affiliate(affiliate_id: str) -> None:
    """
    Tries to add an affiliate to the affiliate list, if it already exists raises an exception
    Or if affiliate doesn't meet the requirements, it also raises an exception

    :param affiliate_id:
    :return:
    """
    affiliate = await bybit.get_affiliate(affiliate_id)

    if affiliate.user_id == '-1':
        raise InvalidAffiliateException

    if affiliate.trade_volume < env.MIN_TRADE_VOLUME:
        raise NotEnoughTradingVolumeException

    if affiliate.deposit < env.MIN_DEPOSIT:
        raise NotEnoughDepositException

    already_joined = await _is_affiliate_already_joined(affiliate.user_id)

    if already_joined:
        raise AffiliateAlreadyExists

    await client.rpush('affiliates', affiliate.user_id)
