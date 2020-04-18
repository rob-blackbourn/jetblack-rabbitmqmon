"""VHost Binding"""

from typing import Any, List, Mapping
from .api import Api


class VHostBinding:
    """A RabbitMQ VHost binding"""

    def __init__(
            self,
            api: Api,
            vhost: str,
            source: str,
            destination: str,
            destination_type: str,
            routing_key: str,
            arguments: Mapping[str, Any],
            properties_key: str
    ):
        """A RabbitMQ VHost binding

        Args:
            api (Api): The api
            vhost (str): The name of the virtual host
            source (str): The source name
            destination (str): The destination name
            destination_type (str): The destination type
            routing_key (str): The routing key
            arguments (Mapping[str, Any]): The arguments
            properties_key (str): The properties key

        Attributes:
            vhost (str): The name of the virtual host
            source (str): The source name
            destination (str): The destination name
            destination_type (str): The destination type
            routing_key (str): The routing key
            arguments (Mapping[str, Any]): The arguments
            properties_key (str): The properties key
        """
        self._api = api
        self.vhost = vhost
        self.source = source
        self.destination = destination
        self.destination_type = destination_type
        self.routing_key = routing_key
        self.arguments = arguments
        self.properties_key = properties_key

    async def props(self) -> List[Mapping[str, Any]]:
        """Fetch the binding properties

        Raises:
            ValueError: If the properties could not be fetched

        Returns:
            List[Mapping[str, Any]]: The binding properties
        """
        if self.destination_type == 'queue':
            props = await self._api.get_vhost_exchange_queue_binding_props(
                self.vhost,
                self.source,
                self.destination,
                self.properties_key
            )
        elif self.destination_type == 'exchange':
            props = await self._api.get_vhost_exchange_exchange_binding_props(
                self.vhost,
                self.source,
                self.destination,
                self.properties_key
            )
        else:
            raise ValueError(
                'Invalid source and destination type combination')
        return props

    def __str__(self) -> str:
        return '<VHostBinding {vhost}:{source} {destination}:{destination_type}>'.format(
            vhost=self.vhost,
            source=self.source,
            destination=self.destination,
            destination_type=self.destination_type
        )

    def __repr__(self) -> str:
        return str(self)
