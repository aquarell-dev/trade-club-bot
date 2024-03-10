from aiogram.client.session import aiohttp


class Exchange:
    def __init__(self, api_key: str, api_secret: str, *, base_url: str) -> None:
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url

    def get_affiliate(self, user_id: int) -> str | None:
        raise NotImplementedError()

    async def _request(
        self,
        url: str,
        method: str,
        *,
        headers: dict = None,
        payload: dict = None,
        query: dict = None
    ) -> dict | None:
        headers = {
            'Content-Type': 'application/json',
            **(headers or {}),
            **self._get_headers(method, payload or query)
        }

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                self._base_url + url,
                headers=headers,
                json=payload,
                params=query
            ) as response:
                return await response.json()

    def _get_headers(self, method: str, payload: dict) -> dict:
        raise NotImplementedError()

    def _generate_signature(self, payload: dict, timestamp: int) -> str:
        raise NotImplementedError()
