"""API"""

from base64 import b64encode
import json
from typing import Mapping, Any, Optional, List
from urllib.parse import quote, urlparse, urlencode

from bareclient import HttpClient
from bareclient.helpers import USER_AGENT
from bareutils import text_reader, bytes_writer, response_code
from .version import Version


def _quote(value):
    return quote(value, '')


class Client:
    """An HTTP client"""

    def __init__(
            self,
            url: str,
            username: str,
            password: str,
            cafile: Optional[str] = '/etc/ssl/certs/ca-certificates.crt'
    ):
        """An HTTP client

        Args:
            url (str): The RabbitMQ url
            username (str): The username
            password (str): The password
            cafile (Optional[str], optional): The certificate file. Defaults
                to '/etc/ssl/certs/ca-certificates.crt'.
        """
        self._management_version: Optional[Version] = None

        self._base_url = f'{url}/api'

        auth = b64encode(f'{username}:{password}'.encode())
        authorization = b'Basic ' + auth

        self._headers_async = [
            (b'host', urlparse(url).hostname.encode('ascii')),
            (b'authorization', authorization),
            (b'content-type', b'application/json'),
            (b'user-agent', USER_AGENT),
            (b'connection', 'close')  # TODO: Try keep-alive
        ]

        self.cafile = cafile

    def _build_url(self, *args: str) -> str:
        quoted_args = map(_quote, args)
        return f"{self._base_url}/{'/'.join(quoted_args)}"

    async def _request(
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
        url = self._build_url(
            *args) + ('?' + urlencode(params) if params else '')
        if not data:
            headers = self._headers_async
            content = None
        else:
            buf = json.dumps(data).encode('utf-8')
            content = bytes_writer(buf)
            headers = self._headers_async + [
                (b'content-length', str(len(buf)).encode('ascii'))
            ]

        async with HttpClient(
                url,
                method=method,
                headers=headers,
                content=content,
                cafile=self.cafile
        ) as response:
            if response_code.is_successful(response['status_code']):
                text = await text_reader(response['body'])
                result = json.loads(text) if text else None
                return result

        raise ValueError('Request failed')

    async def get(
            self,
            *args: str,
            data: Optional[Any] = None,
            params: Optional[Any] = None
    ) -> Optional[Any]:
        """Make a GET request

        Args:
            data (Optional[Any], optional): Used for the body. Defaults to None.
            params (Optional[Any], optional): Used for a querystring. Defaults to None.

        Raises:
            ValueError: If the request fails

        Returns:
            Optional[Any]: The JSON decoded response.
        """
        return await self._request('GET', *args, data=data, params=params)

    async def get_list(
            self,
            *args: str,
            data: Optional[Any] = None,
            params: Optional[Any] = None
    ) -> Optional[List[Mapping[str, Any]]]:
        """Make a GET request returning a list.

        Args:
            data (Optional[Any], optional): Used for the body. Defaults to None.
            params (Optional[Any], optional): Used for a querystring. Defaults to None.

        Raises:
            ValueError: If the request fails

        Returns:
            Optional[Any]: The JSON decoded response.
        """
        return await self.get(*args, data=data, params=params)

    async def get_object(
            self,
            *args: str,
            data: Optional[Any] = None,
            params: Optional[Any] = None
    ) -> Optional[Mapping[str, Any]]:
        """Make a GET request returning an object.

        Args:
            data (Optional[Any], optional): Used for the body. Defaults to None.
            params (Optional[Any], optional): Used for a querystring. Defaults to None.

        Raises:
            ValueError: If the request fails

        Returns:
            Optional[Any]: The JSON decoded response.
        """
        return await self.get(*args, data=data, params=params)

    async def put(
            self,
            *args: str,
            data: Optional[Any] = None,
            params: Optional[Any] = None
    ) -> Optional[Any]:
        """Make a PUT request

        Args:
            data (Optional[Any], optional): Used for the body. Defaults to None.
            params (Optional[Any], optional): Used for a querystring. Defaults to None.

        Raises:
            ValueError: If the request fails

        Returns:
            Optional[Any]: The JSON decoded response.
        """
        return await self._request('PUT', *args, data=data, params=params)

    async def post(
            self,
            *args: str,
            data: Optional[Any] = None,
            params: Optional[Any] = None
    ) -> Optional[Any]:
        """Make a POST request

        Args:
            data (Optional[Any], optional): Used for the body. Defaults to None.
            params (Optional[Any], optional): Used for a querystring. Defaults to None.

        Raises:
            ValueError: If the request fails

        Returns:
            Optional[Any]: The JSON decoded response.
        """
        return await self._request('POST', *args, data=data, params=params)

    async def delete(
            self,
            *args: str,
            data: Optional[Any] = None,
            params: Optional[Any] = None
    ) -> Optional[Any]:
        """Make a DELETE request

        Args:
            data (Optional[Any], optional): Used for the body. Defaults to None.
            params (Optional[Any], optional): Used for a querystring. Defaults to None.

        Raises:
            ValueError: If the request fails

        Returns:
            Optional[Any]: The JSON decoded response.
        """
        return await self._request('DELETE', *args, data=data, params=params)
