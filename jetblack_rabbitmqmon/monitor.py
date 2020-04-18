"""Monitor"""

from typing import List, Mapping, cast

from .requester import Requester
from .api import Api
from .version import Version
from .vhost import VHost
from .channel import Channel
from .connection import Connection
from .node import Node
from .user import User


class Monitor:

    def __init__(
            self,
            requester: Requester
    ):
        self._api = Api(requester)

    async def overview(self):
        return await self._api.get_overview()

    async def management_version(self) -> Version:
        return await self._api.management_version()

    async def cluster_name(self) -> str:
        response = await self._api.get_cluster_name()
        return cast(str, response['name'])

    async def vhosts(self) -> Mapping[str, VHost]:
        response = await self._api.get_vhosts()
        return {
            item['name']: VHost(self._api, **item)
            for item in response
        }

    async def channels(self) -> List[Channel]:
        response = await self._api.get_channels()
        return [
            Channel(self._api, **item)
            for item in response
        ]

    async def connections(self) -> List[Connection]:
        response = await self._api.get_connections()
        return [
            Connection(self._api, **item)
            for item in response
        ]

    async def nodes(self) -> List[Node]:
        response = await self._api.get_nodes()
        return [
            Node(self._api, **item)
            for item in response
        ]

    async def users(self) -> List[User]:
        response = await self._api.get_users()
        return [
            User(self._api, **item)
            for item in response
        ]
