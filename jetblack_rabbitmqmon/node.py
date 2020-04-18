"""Node"""

from __future__ import annotations

from typing import Any, Mapping

from .api import Api


class Node:
    """A rabbitmq node"""

    def __init__(self, api: Api, **kwargs):
        """A RabbitMQ Node

        Attributes:
            name (str): The node name.
            type (str): The node type.
            metrics (Mapping[str, Any]): The node metrics
        """
        self._api = api
        self._init(**kwargs)

    def _init(
            self,
            name: str,
            type: str,  # pylint: disable=redefined-builtin
            **metrics
    ) -> Node:
        self.name = name
        self.type = type
        self.metrics: Mapping[str, Any] = metrics
        return self

    async def refresh(self, memory: bool = False, binary: bool = False) -> Node:
        """Refresh the nodes metrics

        Returns:
            Node: The refreshed node.
        """
        response = await self._api.get_node(self.name, memory, binary)
        return self._init(**response)

    def __str__(self) -> str:
        return '<Node {name}:{type} - {metrics}>'.format(
            name=self.name,
            type=self.type,
            metrics=self.metrics
        )

    def __repr__(self) -> str:
        return str(self)
