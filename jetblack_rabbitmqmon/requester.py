"""API"""

from abc import ABCMeta, abstractmethod
from typing import Mapping, Any, Optional, List
from urllib.parse import quote


def _quote(value):
    return quote(value, '')


class Requester(metaclass=ABCMeta):
    """An HTTP requester"""

    @abstractmethod
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
        return await self.request('GET', *args, data=data, params=params)

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
        return await self.request('PUT', *args, data=data, params=params)

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
        return await self.request('POST', *args, data=data, params=params)

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
        return await self.request('DELETE', *args, data=data, params=params)
