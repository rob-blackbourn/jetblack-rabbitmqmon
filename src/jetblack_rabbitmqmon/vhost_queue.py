"""VHost Queue"""

from __future__ import annotations

from typing import Any, List, Mapping, Optional

from .api import Api
from .vhost_binding import VHostBinding
from .message import Message


class VHostQueue:
    """A RabbitMQ VHost queue"""

    def __init__(self, api: Api, **kwargs):
        """A RabbitMQ VHost queue

        Args:
            api (Api): The API

        Attributes:
            vhost (str): The name of the virtual host
            name (str): The name of the queue
            durable (bool): True if the queue is durable.
            auto_delete (bool): True if the queue will auto delete
            arguments (Mapping[str, Any]): The queue arguments
            node (str): The node name
        """
        self._api = api
        self._init(**kwargs)

    def _init(
            self,
            vhost: str,
            name: str,
            durable: bool,
            auto_delete: bool,
            arguments: Mapping[str, Any],
            node: str,
            **metrics
    ) -> VHostQueue:
        self.vhost = vhost
        self.name = name
        self.node = node
        self.durable = durable
        self.auto_delete = auto_delete
        self.arguments = arguments
        self.metrics: Mapping[str, Any] = metrics
        return self

    async def refresh(self) -> VHostQueue:
        """Refresh the queues metrics

        Returns:
            VHostQueue: The refreshed queue.
        """
        response = await self._api.get_vhost_queue(
            self.vhost,
            self.name
        )
        return self._init(**response)

    async def create_binding(
            self,
            exchange: str,
            routing_key: str,
            arguments: Mapping[str, Any] | None = None
    ) -> None:
        """Create a binding for the queue

        Args:
            exchange (str): The name of the exchange to bind to.
            routing_key (str): The routing key for the binding.

        Returns:
            VHostBinding: The created binding.
        """
        await self._api.create_vhost_exchange_queue_binding(
            self.vhost,
            exchange,
            self.name,
            routing_key,
            arguments
        )

    async def delete_binding(
            self,
            exchange: str,
            props: str
    ) -> None:
        await self._api.delete_vhost_exchange_queue_binding_props(
            self.vhost,
            exchange,
            self.name,
            props
        )

    async def bindings(self) -> List[VHostBinding]:
        """Get the queues bindings

        Returns:
            List[VHostBinding]: A list of bindings.
        """
        response = await self._api.get_vhost_queue_bindings(
            self.vhost,
            self.name
        )
        return [
            VHostBinding(self._api, **item)
            for item in response
        ]

    async def get_messages(
            self,
            count: int = 1,
            requeue: bool = True,
            encoding: str = 'auto',
            truncate: Optional[int] = None,
            reject: bool = False
    ) -> List[Message]:
        """Get messages from the queue

        Args:
            count (int, optional): The number of messages to get. Defaults to 1.
            requeue (bool, optional): Whether to requeue the message. Defaults to True.
            encoding (str, optional): The message encoding. Defaults to 'auto'.
            truncate (Optional[int], optional): The amount to truncate the
                payload. Defaults to None.
            reject (bool, optional): Whether to reject the message. Defaults to False.

        Returns:
            List[Message]: A list of messages.
        """
        response = await self._api.get_vhost_queue_messages(
            self.vhost,
            self.name,
            count,
            requeue,
            encoding,
            truncate,
            reject
        )
        return [
            Message(**item)
            for item in response
        ]

    async def purge(self) -> None:
        """Purge all messages from the queue
        """
        await self._api.purge_vhost_queue(self.vhost, self.name)

    async def delete(
            self,
            if_empty: bool = True,
            if_unused: bool = True
    ) -> None:
        """Delete the queue

        Args:
            if_empty (bool, optional): If true, only delete if empty. Defaults
                to True.
            if_unused (bool, optional): If true, only delete if unused. Defaults
                to True.
        """
        await self._api.delete_vhost_queue(self.vhost, self.name, if_empty, if_unused)

    def __str__(self) -> str:
        return '<VHostQueue {vhost}:{name} - {metrics}>'.format(
            vhost=self.vhost,
            name=self.name,
            metrics=self.metrics
        )

    def __repr__(self) -> str:
        return str(self)
