"""Message"""

from typing import Any, Mapping


class Message:
    """A RabbitMQ message"""

    def __init__(
            self,
            exchange: str,
            routing_key: str,
            redelivered: bool,
            message_count: int,
            payload_encoding: str,
            payload_bytes: int,
            payload: str,
            properties: Mapping[str, Any]
    ):
        """A RabbitMQ message.

        Args:
            exchange (str): The exchange name
            routing_key (str): The routing key
            redelivered (bool): True if the message was relivered.
            message_count (int): The message count
            payload_encoding (str): The payload encoding
            payload_bytes (int): The length of the payload in bytes
            payload (str): The payload
            properties (Mapping[str, Any]): The published properties

        Attributes:
            exchange (str): The exchange name
            routing_key (str): The routing key
            redelivered (bool): True if the message was relivered.
            message_count (int): The message count
            payload_encoding (str): The payload encoding
            payload_bytes (int): The length of the payload in bytes
            payload (str): The payload
            properties (Mapping[str, Any]): The published properties
        """
        self.exchange = exchange
        self.routing_key = routing_key
        self.redelivered = redelivered
        self.message_count = message_count
        self.payload_encoding = payload_encoding
        self.payload_bytes = payload_bytes
        self.payload = payload
        self.properties = properties

    def __str__(self) -> str:
        return '<Message {exchange}:{routing_key} - {payload}>'.format(
            exchange=self.exchange,
            routing_key=self.routing_key,
            payload=self.payload
        )

    def __repr__(self) -> str:
        return str(self)
