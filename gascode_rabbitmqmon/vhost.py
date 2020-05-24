"""VHost"""

from __future__ import annotations

from typing import Any, Mapping, Optional

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
            if item['name']
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
            if item['name']
        }

    async def create_exchange(
            self,
            name: str,
            exchange_type: str,
            durable: bool,
            auto_delete: bool,
            internal: bool,
            arguments: Optional[Mapping[str, Any]] = None
    ) -> VHostExchange:
        """Create an exchange.

        Args:
            name (str): The exchange name
            exchange_type (str): The exchange type
            auto_delete (bool): If true, the exchange will delete itself after
                at least one queue or exchange has been bound to this one, and
                then all queues or exchanges have been unbound.
            durable (bool): If true, the exchange will exists if the server is
                restarted.
            internal (bool): If true, clients cannot publish to this exchange
                directly. It can only be used with exchange to exchange
                bindings.
            arguments (Optional[Mapping[str, Any]], optional): Additional
                arguments. Defaults to None.

        Returns:
            VHostExchange: The created exchange.
        """
        await self._api.create_vhost_exchange(
            self.name,
            name,
            exchange_type,
            durable,
            auto_delete,
            internal,
            arguments
        )
        response = await self._api.get_vhost_exchange(self.name, name)
        return VHostExchange(self._api, **response)

    async def create_queue(
        self,
        name: str,
        durable: Optional[bool] = None,
        auto_delete: Optional[bool] = None,
        arguments: Optional[Mapping[str, Any]] = None,
        node: Optional[str] = None
    ) -> VHostQueue:
        """Create a queue.

        Args:
            name (str): The name of the queue.
            durable (Optional[bool], optional): True if the queue is durable. Defaults to None.
            auto_delete (Optional[bool], optional): True if the queue automatically deletes. Defaults to None.
            arguments (Optional[Mapping[str, Any]], optional): The arguments. Defaults to None.
            node (Optional[str], optional): The node. Defaults to None.

        Returns:
            VHostQueue: The created host.
        """
        await self._api.create_vhost_queue(
            self.name,
            name,
            durable,
            auto_delete,
            arguments,
            node
        )
        response = await self._api.get_vhost_queue(self.name, name)
        return VHostQueue(self._api, **response)

    async def delete(self) -> None:
        """Delete the vhost
        """
        await self._api.delete_vhost(self.name)

    def __str__(self) -> str:
        return '<VHost {name} - {metrics}>'.format(
            name=self.name,
            metrics=self.metrics
        )

    def __repr__(self) -> str:
        return str(self)
