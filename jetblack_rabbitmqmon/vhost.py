"""VHost"""

from __future__ import annotations

from typing import Any, Mapping

from .api import Api
from .vhost_exchange import VHostExchange
from .vhost_queue import VHostQueue


class VHost:
    """A RabbitMQ VHost"""

    def __init__(self, api: Api, **kwargs):
        """A RabbitMQ VHost.

        Args:
            api (Api): The api

        Attribute:
            name (str): The name of the virtual host
            metrics (Mapping[str, Any]): The metrics
        """
        self._api = api
        self._init(**kwargs)

    def _init(self, name: str, **metrics) -> VHost:
        self.name = name
        self.metrics: Mapping[str, Any] = metrics
        return self

    async def refresh(self) -> VHost:
        """Refresh the metrics of the VHost

        Returns:
            VHost: The refresh vhost.
        """
        response = await self._api.get_vhost(self.name)
        return self._init(**response)

    async def exchanges(self) -> Mapping[str, VHostExchange]:
        """Get the VHost exchanges

        Returns:
            Mapping[str, VHostExchange]: A list of exchanges.
        """
        response = await self._api.get_vhost_exchanges(self.name)
        return {
            item['name']: VHostExchange(self._api, **item)
            for item in response
        }

    async def queues(self) -> Mapping[str, VHostQueue]:
        """Get the queues

        Returns:
            Mapping[str, VHostQueue]: A list of queues.
        """
        response = await self._api.get_vhost_queues(self.name)
        return {
            item['name']: VHostQueue(self._api, **item)
            for item in response
        }

    def __str__(self) -> str:
        return '<VHost {name} - {metrics}>'.format(
            name=self.name,
            metrics=self.metrics
        )

    def __repr__(self) -> str:
        return str(self)
