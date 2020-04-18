"""VHost Exchange"""

from __future__ import annotations

from typing import Any, List, Mapping

from .api import Api
from .vhost_binding import VHostBinding


class VHostExchange:
    """A RabbitMQ VHost exchange"""

    def __init__(
            self,
            api: Api,
            **kwargs
    ):
        """A RabbitMQ exchange

        Args:
            api (Api): The API

        Attributes:
            vhost (str): The name of the virtual host
            name (str): The exchange name
            type (str): The exchange type
            auto_delete (bool): True if the exchange will auto delete
            internal (bool): True if the exchange is internal
            arguments (Mapping[str, Any]): The arguments
        """
        self._api = api
        self._init(**kwargs)

    def _init(
            self,
            vhost: str,
            name: str,
            type: str,  # pylint: disable=redefined-builtin
            durable: bool,
            auto_delete: bool,
            internal: bool,
            arguments: Mapping[str, Any],
            **metrics
    ) -> VHostExchange:
        self.vhost = vhost
        self.name = name
        self.type = type
        self.durable = durable
        self.auto_delete = auto_delete
        self.internal = internal
        self.arguments = arguments
        self.metrics: Mapping[str, Any] = metrics
        return self

    async def refresh(self) -> VHostExchange:
        """Refresh the exchange metrics

        Returns:
            VHostExchange: The refreshed exchange.
        """
        response = await self._api.get_vhost_exchange(self.vhost, self.name)
        return self._init(**response)

    async def bindings(self) -> List[VHostBinding]:
        """Get the exchange bindings

        Returns:
            List[VHostBinding]: A list of bindings.
        """
        response = await self._api.get_vhost_exchange_bindings_source(
            self.vhost,
            self.name
        )
        return [
            VHostBinding(self._api, **item)
            for item in response
        ]

    def __str__(self) -> str:
        return '<VHostExchange {vhost}:{name} - {metrics}>'.format(
            vhost=self.vhost,
            name=self.name,
            metrics=self.metrics
        )

    def __repr__(self) -> str:
        return str(self)
