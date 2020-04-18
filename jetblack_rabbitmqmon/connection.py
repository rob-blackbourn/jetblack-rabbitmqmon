"""Connection"""

from __future__ import annotations

from typing import Any, List, Mapping, Optional

from .api import Api
from .channel import Channel


class Connection:
    """A RabbitMQ connection"""

    def __init__(
            self,
            api: Api,
            **kwargs
    ):
        """A RabbitMQ connection

        Args:
            api (Api): The api.

        Attributes:
            node (str): The node name
            vhost (str): The name of the virtual host
            name (str): The connection name
            user (str): Th user name
            protocol (str): The protocol
            type (str): The connection type
            host (str): The host name
            port (int): The host port
            peer_host (str): The peer host name
            peer_port (int): The peer host port
            client_properties (Mapping[str, Any]): The client properties
            auth_mechanism (str): The authentication mechanism used
            ssl (bool): True if using ssl
            ssl_hash (Optional[str]): The ssl hash
            ssl_cipher (Optional[str]): The ssl cipher
            ssl_protocol (Optional[str]): The ssl protocol
            peer_cert_validity (Optional[str]): The peer certificate validity
            peer_cert_issuer (Optional[str]): The peer certificate issuer
            peer_cert_subject (Optional[str]): The peer certificate subject name
        """
        self._api = api
        self._init(**kwargs)

    def _init(
            self,
            node: str,
            vhost: str,
            name: str,
            user: str,
            protocol: str,
            type: str,  # pylint: disable=redefined-builtin
            host: str,
            port: int,
            peer_host: str,
            peer_port: int,
            client_properties: Mapping[str, Any],
            auth_mechanism: str,
            ssl: bool,
            ssl_hash: Optional[str],
            ssl_cipher: Optional[str],
            ssl_protocol: Optional[str],
            peer_cert_validity: Optional[str],
            peer_cert_issuer: Optional[str],
            peer_cert_subject: Optional[str],
            **metrics
    ) -> Connection:
        self.node = node
        self.vhost = vhost
        self.name = name
        self.user = user
        self.host = host
        self.port = port
        self.peer_host = peer_host
        self.peer_port = peer_port
        self.protocol = protocol
        self.type = type
        self.client_properties = client_properties
        self.ssl = ssl
        self.ssl_hash = ssl_hash
        self.ssl_cipher = ssl_cipher
        self.ssl_protocol = ssl_protocol
        self.auth_mechanism = auth_mechanism
        self.peer_cert_validity = peer_cert_validity
        self.peer_cert_issuer = peer_cert_issuer
        self.peer_cert_subject = peer_cert_subject
        self.metrics: Optional[Mapping[str, Any]] = metrics
        return self

    async def refresh(self) -> Connection:
        """Refresh the connection

        Returns:
            Connection: The refreshed connection
        """
        response = await self._api.get_connection(self.name)
        return self._init(**response)

    async def channels(self) -> List[Channel]:
        """Get the channels

        Returns:
            List[Channel]: A list of channels
        """
        response = await self._api.get_connection_channels(self.name)
        return [
            Channel(self._api, **item)
            for item in response
        ]

    def __str__(self) -> str:
        return '<Connection {node} {vhost}:{name} - {metrics}>'.format(
            node=self.node,
            vhost=self.vhost,
            name=self.name,
            metrics=self.metrics
        )

    def __repr__(self) -> str:
        return str(self)
