from redis_client import client


class AffiliateException(Exception):
    def __init__(self, key: str):
        self._key = key

    async def get_message(self) -> str:
        return await client.get(self._key)


class AffiliateAlreadyExists(AffiliateException):
    def __init__(self):
        super().__init__('affiliate_already_exists')


class InvalidAffiliateException(AffiliateException):
    def __init__(self):
        super().__init__('affiliate_not_found')


class NotEnoughDepositException(AffiliateException):
    def __init__(self):
        super().__init__('not_enough_deposit')


class NotEnoughTradingVolumeException(AffiliateException):
    def __init__(self):
        super().__init__('not_enough_trading_volume')
