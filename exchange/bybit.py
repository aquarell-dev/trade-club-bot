import hashlib
import hmac
import json
import time

from affiliate import Affiliate
from affiliate.exceptions import (
    InvalidAffiliateException,
    NotEnoughDepositException,
    NotEnoughTradingVolumeException
)
from exchange import Exchange
from settings import get_env

env = get_env()


class Bybit(Exchange):
    def __init__(self):
        super().__init__(
            env.BYBIT_API_PUBLIC_KEY,
            env.BYBIT_API_SECRET_KEY,
            base_url=env.BYBIT_BASE_API_URL
        )
        self._recv_window = '5000'

    async def get_affiliate(self, user_id: str) -> Affiliate:
        response = await self._request(
            'user/aff-customer-info',
            'GET',
            query={'uid': user_id}
        )

        affiliate_data = response.get('result', {})

        affiliate_id = affiliate_data.get('uid', '-1')
        trade_volume = float(affiliate_data.get('tradeVol365Day', 0))
        deposit = float(affiliate_data.get('depositAmount365Day', 0))

        if response.get('retCode', -1) != 0 or affiliate_id == '-1':
            raise InvalidAffiliateException()

        if trade_volume < env.MIN_TRADE_VOLUME:
            raise NotEnoughTradingVolumeException(env.MIN_TRADE_VOLUME)

        if deposit < env.MIN_DEPOSIT:
            raise NotEnoughDepositException(env.MIN_DEPOSIT)

        return Affiliate(
            user_id=affiliate_id,
            trade_volume=trade_volume,
            deposit=deposit
        )

    def _get_headers(self, method: str, payload: dict) -> dict:
        timestamp = int(time.time() * 10 ** 3)

        if method == 'GET':
            payload = self._payload_to_query(payload)
        else:
            payload = json.dumps(payload)

        return {
            'X-BAPI-API-KEY': self._api_key,
            'X-BAPI-SIGN': self._generate_signature(payload, timestamp),
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': str(timestamp),
            'X-BAPI-RECV-WINDOW': self._recv_window,
        }

    def _generate_signature(self, payload: str, timestamp: int) -> str:
        params = str(timestamp) + self._api_key + self._recv_window + payload
        hashed = hmac.new(bytes(self._api_secret, "utf-8"), params.encode("utf-8"), hashlib.sha256)
        return hashed.hexdigest()

    def _payload_to_query(self, payload: dict) -> str:
        return '&'.join([f'{k}={v}' for k, v in payload.items()])
