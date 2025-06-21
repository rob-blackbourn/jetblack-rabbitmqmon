"""aiohttp requester"""

import json
import ssl
from typing import Any, Optional
from urllib.parse import quote

from httpx import AsyncClient, BasicAuth

from ..requester import Requester

def _quote(value):
    return quote(value, '')


class HttpxRequester(Requester):
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
            cafile (Optional[str], optional): The certificate file. Defaults
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
            data: Optional[Any] = None,
            params: Optional[Any] = None
    ) -> Optional[Any]:
        """Make an HTTP request

        Args:
            method (str): The HTTP method
            data (Optional[Any], optional): Used for the body. Defaults to None.
            params (Optional[Any], optional): Used for a querystring. Defaults to None.

        Raises:
            ValueError: If the request fails

        Returns:
            Optional[Any]: The JSON decoded response.
        """

        url = self._build_url(*args)
        params_as_str = {
            name: json.dumps(value)
            for name, value in params.items()
        } if params else None

        async with AsyncClient(auth=self.auth, verify=self.ssl_context) as session:
            response = await session.request(
                    method,
                    url,
                    params=params_as_str,
                    json=data,
            )
            response.raise_for_status()
            body = response.json()
            return body

        raise ValueError('Request failed')
