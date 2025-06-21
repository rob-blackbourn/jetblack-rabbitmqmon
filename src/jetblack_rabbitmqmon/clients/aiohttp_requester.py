"""aiohttp requester"""

import json
import ssl
from typing import Any
from urllib.parse import quote

from aiohttp import ClientSession, BasicAuth

from ..requester import Requester


def _quote(value):
    return quote(value, '')


class AioHttpRequester(Requester):
    """An HTTP client"""

    def __init__(
            self,
            url: str,
            username: str,
            password: str,
            cafile: str | None = None
    ):
        """An HTTP client

        Args:
            url (str): The RabbitMQ url
            username (str): The username
            password (str): The password
            cafile (str | None, optional): The certificate file. Defaults
                to '/etc/ssl/certs/ca-certificates.crt'.
        """
        self._base_url = f'{url}/api'

        self.auth = BasicAuth(username, password)
        self.ssl_context = ssl.create_default_context(
            cafile=cafile
        ) if cafile else False

    def _build_url(self, *args: str) -> str:
        quoted_args = map(_quote, args)
        return f"{self._base_url}/{'/'.join(quoted_args)}"

    async def request(
            self,
            method: str,
            *args: str,
            data: Any | None = None,
            params: Any | None = None
    ) -> Any | None:
        """Make an HTTP request

        Args:
            method (str): The HTTP method
            data (Any | None, optional): Used for the body. Defaults to None.
            params (Any | None, optional): Used for a querystring. Defaults to None.

        Raises:
            ValueError: If the request fails

        Returns:
            Any | None: The JSON decoded response.
        """

        url = self._build_url(*args)
        params_as_str = {
            name: json.dumps(value)
            for name, value in params.items()
        } if params else None

        async with ClientSession(auth=self.auth) as session:
            async with session.request(
                    method,
                    url,
                    params=params_as_str,
                    json=data,
                    ssl=self.ssl_context
            ) as response:
                if response.status == 200:
                    body = await response.json()
                    return body

        raise ValueError('Request failed')
