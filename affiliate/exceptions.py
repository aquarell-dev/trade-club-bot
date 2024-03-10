from enums import Text


class AffiliateException(Exception):
    def __init__(self, message: str):
        self._message = message

    def get_message(self) -> str:
        return self._message


class InvalidAffiliateException(AffiliateException):
    def __init__(self):
        super().__init__(Text.AFFILIATE_NOT_FOUND)


class NotEnoughDepositException(AffiliateException):
    def __init__(self, min_deposit: int):
        super().__init__(Text.NOT_ENOUGH_DEPOSIT.format(min_deposit))


class NotEnoughTradingVolumeException(AffiliateException):
    def __init__(self, trading_volume: int):
        super().__init__(Text.NOT_ENOUGH_TRADING_VOLUME.format(trading_volume))
