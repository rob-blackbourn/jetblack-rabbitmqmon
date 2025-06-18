"""Channel"""

from __future__ import annotations

from typing import Any, Mapping

from .api import Api


class Channel:
    """A RabbitMQ channel"""

    def __init__(
            self,
            api: Api,
            **kwargs
    ):
        """A RabbitMQ Channel

        Attributes:
            node (str): The node name.
            vhost (str): The name of the virtual host.
            name (str): The name of the channel.
            number (int): The channel number
        """
        self._api = api
        self._init(**kwargs)

    def _init(
        self,
        node: str,
        vhost: str,
        name: str,
        number: int,
        **metrics
    ) -> Channel:
        self.node = node
        self.vhost = vhost
        self.name = name
        self.number = number
        self.metrics: Mapping[str, Any] = metrics
        return self

    async def refresh(self) -> Channel:
        """Refresh the channel metrics

        Returns:
            Channel: The refresh channel.
        """
        response = await self._api.get_channel(self.name)
        return self._init(**response)

    def __str__(self) -> str:
        return '<Channel {vhost}:{name}({number}) - {metrics}>'.format(
            vhost=self.vhost,
            name=self.name,
            number=self.number,
            metrics=self.metrics
        )

    def __repr__(self) -> str:
        return str(self)
