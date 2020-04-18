"""Api"""

from typing import Any, List, Mapping, Optional

from .requester import Requester
from .version import Version


VERSION_3_6 = Version('3.6')
VERSION_3_7 = Version('3.7')


class ApiError(Exception):
    """An API Error"""


class Api:
    """The RabbitMQ REST api"""

    def __init__(
            self,
            requester: Requester

    ):
        self._requester = requester
        self._management_version: Optional[Version] = None

    async def management_version(self) -> Version:

        if self._management_version is None:
            overview = await self.get_overview()
            self._management_version = Version(overview['management_version'])
        return self._management_version

    async def get_overview(self) -> Mapping[str, Any]:
        """Various random bits of information that describe the whole system.

        Raises:
            ApiError: If no data was returned.

        Returns:
            Mapping[str, Any]: The information
        """
        response = await self._requester.get_object('overview')
        if response is None:
            raise ApiError
        return response

    async def get_cluster_name(self) -> Mapping[str, Any]:
        """Get the name identifying this RabbitMQ cluster.

        Raises:
            ApiError: If no data was returned

        Returns:
            Mapping[str, Any]: An object containing the cluster name.
        """
        response = await self._requester.get_object('cluster-name')
        if response is None:
            raise ApiError
        return response

    async def set_cluster_name(self, name: str) -> None:
        """Set the name identifying this RabbitMQ cluster.

        Args:
            name (str): The new cluster name

        Raises:
            ApiError: If the name could not be set.
        """
        response = await self._requester.put('cluster-name', data={'name': name})
        if response is not None:
            raise ApiError(response)

    async def get_nodes(self) -> List[Mapping[str, Any]]:
        """A list of nodes in the RabbitMQ cluster.

        Raises:
            ApiError: If no data was returned

        Returns:
            List[Mapping[str, Any]]: The list of nodes
        """
        response = await self._requester.get_list('nodes')
        if response is None:
            raise ApiError
        return response

    async def get_node(
            self,
            name: str,
            memory: bool = False,
            binary: bool = False
    ) -> Mapping[str, Any]:
        """An individual node in the RabbitMQ cluster. Add "?memory=true" to get
        memory statistics, and "?binary=true" to get a breakdown of binary
        memory use (may be expensive if there are many small binaries in the
        system).


        Args:
            name (str): The name of the node

        Raises:
            ApiError: When no data is returned.

        Returns:
            List[Mapping[str, Any]]: The node details.
        """
        params = {
            'memory': memory,
            'binary': binary
        }
        response = await self._requester.get_object('nodes', name, params=params)
        if response is None:
            raise ApiError
        return response

    async def get_extensions(self) -> List[Mapping[str, Any]]:
        """A list of extensions to the management plugin.

        Raises:
            ApiError: [description]

        Returns:
            List[Mapping[str, Any]]: The list of extensions
        """
        response = await self._requester.get_list('extensions')
        if response is None:
            raise ApiError
        return response

    async def get_definitions(self) -> Mapping[str, Any]:
        """The server definitions - exchanges, queues, bindings, users, virtual
        hosts, permissions, topic permissions, and parameters. Everything apart
        from messages. POST to upload an existing set of definitions.

        Note that:
            The definitions are merged. Anything already existing on the server
            but not in the uploaded definitions is untouched.

            Conflicting definitions on immutable objects (exchanges, queues and
            bindings) will cause an error.

            Conflicting definitions on mutable objects will cause the object in
            the server to be overwritten with the object from the definitions.

            In the event of an error you will be left with a part-applied set of
            definitions.

            For convenience you may upload a file from a browser to this URI
            (i.e. you can use multipart/form-data as well as application/json)
            in which case the definitions should be uploaded as a form field
            named "file".


        Raises:
            ApiError: [description]

        Returns:
            Mapping[str, Any]: The definitions.
        """
        response = await self._requester.get_object('definitions')
        if response is None:
            raise ApiError
        return response

    async def set_definitions(self, definitions: Mapping[str, Any]) -> None:
        """Set the server definitions.

        Args:
            definitions (Mapping[str, Any]): The definitions

        Raises:
            ApiError: If the operation failed
        """
        response = await self._requester.put('definitions', data=definitions)
        if response is not None:
            raise ApiError(response)

    async def get_vhost_definitions(self, vhost: str) -> Mapping[str, Any]:
        """The server definitions for a vhost

        Raises:
            ApiError: [description]

        Returns:
            Mapping[str, Any]: The definitions.
        """
        response = await self._requester.get_object('definitions', vhost)
        if response is None:
            raise ApiError
        return response

    async def get_connections(self) -> List[Mapping[str, Any]]:
        """A list of all open connections.


        Raises:
            ApiError: If the operation failed

        Returns:
            List[Mapping[str, Any]]: A list of connections.
        """
        response = await self._requester.get_list('connections')
        if response is None:
            raise ApiError
        return response

    async def get_vhost_connections(self, vhost: str) -> List[Mapping[str, Any]]:
        """A list of all open connections in a specific vhost.

        Args:
            vhost (str): The name of the vhost.

        Raises:
            ApiError: If the operation failed.

        Returns:
            List[Mapping[str, Any]]: A list of connections
        """
        response = await self._requester.get_list('vhosts', vhost, 'connections')
        if response is None:
            raise ApiError
        return response

    async def get_connection(self, name: str) -> Mapping[str, Any]:
        """An individual connection. DELETEing it will close the connection.
        Optionally set the "X-Reason" header when DELETEing to provide a reason.

        Args:
            name (str): The connection name

        Raises:
            ApiError: [description]

        Returns:
            Mapping[str, Any]: The connection details
        """
        response = await self._requester.get_object('connections', name)
        if response is None:
            raise ApiError
        return response

    async def delete_connection(self, name: str):
        """Delete a connection

        Args:
            name (str): The connection name

        Raises:
            ApiError: [description]

        Returns:
            Mapping[str, Any]: The connection details
        """
        response = await self._requester.delete('connections', name)
        if response is not None:
            raise ApiError

    async def get_connection_channels(self, name: str) -> List[Mapping[str, Any]]:
        """List of all channels for a given connection.

        Args:
            name (str): The connection name

        Raises:
            ApiError: [description]

        Returns:
            List[Mapping[str, Any]]: A list of channels
        """
        response = await self._requester.get_list('connection', name, 'channels')
        if response is None:
            raise ApiError
        return response

    async def get_channels(self) -> List[Mapping[str, Any]]:
        """A list of all open channels.

        Raises:
            ApiError: [description]

        Returns:
            List[Mapping[str, Any]]: A list of channels
        """
        response = await self._requester.get_list('channels')
        if response is None:
            raise ApiError
        return response

    async def get_vhost_channels(self, vhost: str) -> List[Mapping[str, Any]]:
        """A list of all open channels in a specific vhost.

        Args:
            vhost (str): The name of the vhost

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of channel details.
        """
        response = await self._requester.get_list('vhost', vhost, 'channels')
        if response is None:
            raise ApiError
        return response

    async def get_channel(self, channel: str) -> Mapping[str, Any]:
        """Details about an individual channel.

        Args:
            channel (str): The channel name

        Raises:
            ApiError: If the operation fails

        Returns:
            Mapping[str, Any]: The channel details
        """
        response = await self._requester.get_object('channels', channel)
        if response is None:
            raise ApiError
        return response

    async def get_consumers(self) -> List[Mapping[str, Any]]:
        """A list of all consumers.

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of consumers
        """
        response = await self._requester.get_list('consumers')
        if response is None:
            raise ApiError
        return response

    async def get_vhost_consumers(self, vhost: str) -> List[Mapping[str, Any]]:
        """A list of all consumers in a given virtual host.

        Args:
            vhost (str): The vhost name

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of consumers
        """
        response = await self._requester.get_list('consumers', vhost)
        if response is None:
            raise ApiError
        return response

    async def get_exchanges(self) -> List[Mapping[str, Any]]:
        """A list of all exchanges.

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of exchanges
        """
        response = await self._requester.get_list('exchanges')
        if response is None:
            raise ApiError
        return response

    async def get_vhost_exchanges(self, vhost: str) -> List[Mapping[str, Any]]:
        """A list of all exchanges in a given virtual host.

        Args:
            vhost (str): The vhost name

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of exchanges
        """
        response = await self._requester.get_list('exchanges', vhost)
        if response is None:
            raise ApiError
        return response

    async def get_vhost_exchange(self, vhost: str, name: str) -> Mapping[str, Any]:
        """An individual exchange.


        Args:
            vhost (str): The name of the virtual host
            name (str): The exchange name

        Raises:
            ApiError: If the operation fails

        Returns:
            Mapping[str, Any]: The exchange details
        """
        response = await self._requester.get_object('exchanges', vhost, name)
        if response is None:
            raise ApiError
        return response

    async def create_vhost_exchange(
            self,
            vhost: str,
            name: str,
            exchange_type: str,
            auto_delete: bool,
            durable: bool,
            internal: bool,
            arguments: Optional[Mapping[str, Any]] = None
    ) -> None:
        """Create an individual exchange.

        Args:
            vhost (str): The name of the virtual host
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
        """
        data = {
            "type": exchange_type,
            "auto_delete": auto_delete,
            "durable": durable,
            "internal": internal,
            "arguments": arguments or {}
        }
        response = await self._requester.put('exchanges', vhost, name, data=data)
        if response is not None:
            raise ApiError

    async def delete_vhost_exchange(self, vhost: str, name: str, if_unused: bool) -> None:
        """Delete an exchange

        Args:
            vhost (str): The name of the virtual host
            name (str): The exchange name
            if_unused (bool): This prevents the delete from succeeding if the
                exchange is bound to a queue or as a source to another exchange.

        Raises:
            ApiError: [description]
        """
        params = {
            'if-unused': if_unused
        }
        response = await self._requester.delete('exchanges', vhost, name, params=params)
        if response is not None:
            raise ApiError

    async def get_vhost_exchange_bindings_source(self, vhost: str, name: str) -> List[Mapping[str, Any]]:
        """A list of all bindings in which a given exchange is the source.

        Args:
            vhost (str): The name of the virtual host
            name (str): The exchange name

        Raises:
            ApiError: If the operation failed

        Returns:
            List[Mapping[str, Any]]: A list of bindings
        """
        response = await self._requester.get_list('exchanges', vhost, name, 'bindings', 'source')
        if response is None:
            raise ApiError
        return response

    async def get_vhost_exchange_bindings_destination(self, vhost: str, name: str) -> List[Mapping[str, Any]]:
        """A list of all bindings in which a given exchange is the destination.

        Args:
            vhost (str): The name of the virtual host
            name (str): The exchange name

        Raises:
            ApiError: If the operation failed

        Returns:
            List[Mapping[str, Any]]: A list of bindings
        """
        response = await self._requester.get_list('exchanges', vhost, name, 'bindings', 'destination')
        if response is None:
            raise ApiError
        return response

    async def publish_message(
            self,
        vhost: str,
        name: str,
        properties: Mapping[str, Any],
        routing_key: str,
        payload: Any,
        payload_encoding: str
    ) -> Mapping[str, Any]:
        """Publish a message to a given exchange. 

        The payload_encoding key should be either "string" (in which case the
        payload will be taken to be the UTF-8 encoding of the payload field) or
        "base64" (in which case the payload field is taken to be base64 encoded).

        If the message is published successfully, the response will look like:
        {"routed": true}
        routed will be true if the message was sent to at least one queue.
        Please note that the HTTP API is not ideal for high performance publishing;
        the need to create a new TCP connection for each message published can limit
        message throughput compared to AMQP or other protocols using long-lived
        connections.

        Args:
            vhost (str): The name of the virtual host
            name (str): The exchange name
            properties (Mapping[str, Any]): The messages properties
            routing_key (str): The routing key
            payload (Any): The payload
            payload_encoding (str): The payload encoding

        Returns:
            Mapping[str, Any]: Information about publish action.
        """
        data = {
            "properties": properties,
            "routing_key": routing_key,
            "payload": payload,
            "payload_encoding": payload_encoding
        }
        response = await self._requester.post('exchanges', vhost, name, 'publish', data=data)
        if response is None:
            raise ApiError
        return response

    async def get_queues(self) -> List[Mapping[str, Any]]:
        """A list of all queues.

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of queues.
        """
        response = await self._requester.get_list('queues')
        if response is None:
            raise ApiError
        return response

    async def get_vhost_queues(self, vhost: str) -> List[Mapping[str, Any]]:
        """A list of all queues in a given virtual host.

        Args:
            vhost (str): The name of the virtual host

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of queues
        """
        response = await self._requester.get_list('queues', vhost)
        if response is None:
            raise ApiError
        return response

    async def get_vhost_queue(self, vhost: str, name: str) -> Mapping[str, Any]:
        """Get an individual queue.

        Args:
            vhost (str): The name of the virtual host
            name (str): The queue name

        Raises:
            ApiError: THe queue details.

        Returns:
            Mapping[str, Any]: [description]
        """
        response = await self._requester.get_object('queues', vhost, name)
        if response is None:
            raise ApiError
        return response

    async def create_vhost_queue(
            self,
            vhost: str,
            name: str,
            auto_delete: bool,
            durable: bool,
            arguments: Mapping[str, Any],
            node: str
    ) -> None:
        """Create an individual queue.

        Args:
            vhost (str): The name of the virtual host
            name (str): The queue name
            auto_delete (bool): Whether the queue automatically deletes.
            durable (bool): Whether the queue is durable
            arguments (Mapping[str, Any]): Extra arguments
            node (str): The node name
        """
        data = {
            "auto_delete": auto_delete,
            "durable": durable,
            "arguments": arguments,
            "node": node
        }
        response = await self._requester.put('queues', vhost, name, data=data)
        if response is not None:
            raise ApiError

    async def delete_vhost_queue(
            self,
            vhost: str,
            name: str,
            if_empty: bool,
            if_unused: bool
    ) -> None:
        """Delete an individual queue.

        Args:
            vhost (str): The name of the virtual host
            name (str): The queue name
            if_empty (bool): If true only delete if the queue is empty.
            if_unused (bool): If true only delete if the queue has no consumers.

        Raises:
            ApiError: If the operation failed.
        """
        response = await self._requester.delete('queues', vhost, name)
        if response is not None:
            raise ApiError

    async def get_vhost_queue_bindings(self, vhost: str, name: str) -> List[Mapping[str, Any]]:
        """A list of all bindings on a given queue.

        Args:
            vhost (str): The name of the virtual host
            name (str): The queue name

        Raises:
            ApiError: If the operation failed

        Returns:
            List[Mapping[str, Any]]: A list of bindings.
        """
        response = await self._requester.get_list('queues', vhost, name, 'bindings')
        if response is None:
            raise ApiError
        return response

    async def purge_vhost_queue(self, vhost: str, name: str) -> None:
        """Purge the contents of a queue.

        Args:
            vhost (str): The name of the virtual host
            name (str): The queue name

        Raises:
            ApiError: If the operation failed
        """
        response = await self._requester.delete('queue', vhost, name, 'contents')
        if response is not None:
            raise ApiError

    async def invoke_vhost_queue_action(self, vhost: str, name: str, action: str) -> None:
        """Actions that can be taken on a queue.

        Currently the actions which are supported are sync and cancel_sync.

        Args:
            vhost (str): The name of the virtual host
            name (str): The queue name
            action (str): The action to invoke

        Raises:
            ApiError: If the operation failed
        """
        data = {
            'action': action
        }
        response = await self._requester.post('queues', vhost, name, 'actions', data=data)
        if response is not None:
            raise ApiError

    async def get_vhost_queue_messages_36(
            self,
            vhost: str,
            name: str,
            count: int,
            requeue: bool,
            encoding: str = 'auto',
            truncate: Optional[int] = None
    ) -> List[Mapping[str, Any]]:
        data = {
            "count": count,
            "requeue": requeue,
            "encoding": encoding
        }
        if truncate is not None:
            data['truncate'] = truncate
        response = await self._requester.post('queues', vhost, name, 'get', data=data)
        if response is None:
            raise ApiError
        return response

    async def get_vhost_queue_messages(
            self,
            vhost: str,
            name: str,
            count: int = 1,
            requeue: bool = True,
            encoding: str = 'auto',
            truncate: Optional[int] = None,
            reject: bool = False
    ) -> List[Mapping[str, Any]]:
        version = await self.management_version()

        if VERSION_3_6 <= version < VERSION_3_7:
            if reject:
                raise NotImplementedError
            data = {
                'count': count,
                'encoding': encoding,
                'name': name,
                'requeue': requeue,
                'vhost': vhost
            }
        elif version >= VERSION_3_7:
            if requeue:
                if reject:
                    ackmode = 'reject_requeue_true'
                else:
                    ackmode = 'ack_requeue_true'
            else:
                if reject:
                    ackmode = 'reject_requeue_false'
                else:
                    ackmode = 'ack_requeue_false'
            data = {
                'count': count,
                'encoding': encoding,
                'name': name,
                'ackmode': ackmode,
                'vhost': vhost
            }
        else:
            raise Exception('Unhandled version of management plugin')

        if truncate is not None:
            data['truncate'] = truncate

        response = await self._requester.post('queues', vhost, name, 'get', data=data)
        if response is None:
            raise ApiError
        return response

    async def get_vhost_queue_messages_37(
            self,
            vhost: str,
            name: str,
            count: int,
            ackmode: str,
            encoding: str = 'auto',
            truncate: Optional[int] = None
    ) -> List[Mapping[str, Any]]:
        """Get messages from a queue.
        truncate is optional; all other keys are mandatory.

        Please note that the get path in the HTTP API is intended for diagnostics etc - it does not implement reliable delivery and so should be treated as a sysadmin's tool rather than a general API for messaging.

        Args:
            vhost (str): The name of the virtual host
            name (str): The name of the queue
            count (int): Controls the maximum number of messages to get. You may
                 get fewer messages than this if the queue cannot immediately
                 provide them.
            ackmode (str): Determines whether the messages will be removed from
                the queue. If ackmode is ack_requeue_true or reject_requeue_true
                they will be requeued - if ackmode is ack_requeue_false or
                reject_requeue_false they will be removed.
            encoding (str, optional): Must be either "auto" (in which case the
                payload will be returned as a string if it is valid UTF-8, and
                base64 encoded otherwise), or "base64" (in which case the
                payload will always be base64 encoded). Defaults to 'auto'.
            truncate (Optional[int], optional): If truncate is present it will
                truncate the message payload if it is larger than the size given
                (in bytes). Defaults to None.

        Raises:
            ApiError: If the operation failed.

        Returns:
            List[Mapping[str, Any]]: The messages
        """
        data = {
            "count": count,
            "ackmode": ackmode,
            "encoding": encoding
        }
        if truncate is not None:
            data['truncate'] = truncate
        response = await self._requester.post('queues', vhost, name, 'get', data=data)
        if response is None:
            raise ApiError
        return response

    async def get_bindings(self) -> List[Mapping[str, Any]]:
        """A list of all bindings.

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of bindings
        """
        response = await self._requester.get('bindings')
        if response is None:
            raise ApiError
        return response

    async def get_vhost_bindings(self, vhost: str) -> List[Mapping[str, Any]]:
        """A list of all bindings in a given virtual host.

        Args:
            vhost (str): The name of the virtual host.

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of bindings
        """
        response = await self._requester.get('bindings', vhost)
        if response is None:
            raise ApiError
        return response

    async def get_vhost_exchange_queue_bindings(
            self,
            vhost: str,
            exchange: str,
            queue: str
    ) -> List[Mapping[str, Any]]:
        """A list of all bindings between an exchange and a queue. Remember, an
        exchange and a queue can be bound together many times!

        Args:
            vhost (str): The name of the virtual host
            exchange (str): The name of the exchange
            queue (str): The name of the queue

        Raises:
            ApiError: If the operation failed

        Returns:
            List[Mapping[str, Any]]: A list of the bindings
        """
        response = await self._requester.get('bindings', vhost, 'e', exchange, 'q', queue)
        if response is None:
            raise ApiError
        return response

    async def set_vhost_exchange_queue_bindings(
            self,
            vhost: str,
            exchange: str,
            queue: str,
            routing_key: str,
            arguments: List[Mapping[str, Any]]
    ) -> List[Mapping[str, Any]]:
        data = {
            "routing_key": routing_key,
            "arguments": arguments
        }
        response = await self._requester.post(
            'bindings', vhost, 'e', exchange, 'q', queue,
            data=data
        )
        if response is None:
            raise ApiError
        return response

    async def get_vhost_exchange_queue_binding_props(
            self,
            vhost: str,
            exchange: str,
            queue: str,
            props: str
    ) -> List[Mapping[str, Any]]:
        """An individual binding between an exchange and a queue. The props part
        of the URI is a "name" for the binding composed of its routing key and a
        hash of its arguments. props is the field named "properties_key" from a
        bindings listing response.

        Args:
            vhost (str): The name of the virtual host
            exchange (str): The name of the exchange
            queue (str): The name of the queue
            props (str): The properties key

        Raises:
            ApiError: If the operation failed

        Returns:
            List[Mapping[str, Any]]: A list of the binding properties
        """
        response = await self._requester.get('bindings', vhost, 'e', exchange, 'q', queue, props)
        if response is None:
            raise ApiError
        return response

    async def delete_vhost_exchange_queue_binding_props(
            self,
            vhost: str,
            exchange: str,
            queue: str,
            props: str
    ) -> None:
        response = await self._requester.delete(
            'bindings', vhost, 'e', exchange, 'q', queue, props
        )
        if response is not None:
            raise ApiError

    async def get_vhost_exchange_exchange_binding(
            self,
            vhost: str,
            source: str,
            destination: str
    ) -> List[Mapping[str, Any]]:
        """Get a list of all bindings between two exchanges, similar to the list of
        all bindings between an exchange and a queue

        Args:
            vhost (str): The name of the virtual host
            source (str): The source exchange
            destination (str): The destination exchange

        Raises:
            ApiError: If the operation failed

        Returns:
            List[Mapping[str, Any]]: A list of bindings
        """
        response = await self._requester.get('bindings', vhost, 'e', source, 'e', destination)
        if response is None:
            raise ApiError
        return response

    async def create_vhost_exchange_exchange_binding(
            self,
            vhost: str,
            source: str,
            destination: str,
            routing_key: str,
            arguments: Mapping[str, Any]
    ) -> None:
        """Create a binding between two exchanges.

        Args:
            vhost (str): The name of the virtual host
            source (str): The source exchange
            destination (str): The destination exchange
            routing_key (str): The routing key
            arguments (Mapping[str, Any]): Binding arguments.

        Raises:
            ApiError: If the operation fails
        """
        data = {
            "routing_key": routing_key,
            "arguments": arguments
        }
        response = await self._requester.post(
            'bindings', vhost, 'e', source, 'e', destination,
            data=data
        )
        if response is None:
            raise ApiError

    async def get_vhost_exchange_exchange_binding_props(
            self,
            vhost: str,
            source: str,
            destination: str,
            props: str
    ) -> List[Mapping[str, Any]]:
        """Get an individual binding between two exchanges. Similar to the
        individual binding between an exchange and a queue.

        Args:
            vhost (str): The name of the virtual host
            source (str): The name of the source exchange
            destination (str): The name of the destination exchanges
            props (str): The property name

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of the props
        """
        response = await self._requester.get('bindings', vhost, 'e', source, 'e', destination, props)
        if response is None:
            raise ApiError
        return response

    async def delete_vhost_exchange_exchange_binding_props(
            self,
            vhost: str,
            source: str,
            destination: str,
            props: str
    ) -> None:
        """Delete an individual binding between two exchanges. Similar to the
        individual binding between an exchange and a queue.

        Args:
            vhost (str): The name of the virtual host
            source (str): The name of the source exchange
            destination (str): The name of the destination exchanges
            props (str): The property name

        Raises:
            ApiError: If the operation fails
        """
        response = await self._requester.delete(
            'bindings', vhost, 'e', source, 'e', destination, props
        )
        if response is None:
            raise ApiError

    async def get_vhosts(self) -> List[Mapping[str, Any]]:
        """A list of all vhosts.

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of virtual hosts.
        """
        response = await self._requester.get_list('vhosts')
        if response is None:
            raise ApiError
        return response

    async def get_vhost(self, vhost: str) -> Mapping[str, Any]:
        """An individual virtual host

        Args:
            vhost (str): The name of the virtual host.

        Raises:
            ApiError: If the operation fails

        Returns:
            Mapping[str, Any]: The details of the virtual host
        """
        response = await self._requester.get_object('vhost', vhost)
        if response is None:
            raise ApiError
        return response

    async def create_vhost(self, vhost: str, tracing: bool) -> None:
        """Create a virtual host

        Args:
            vhost (str): The name of the virtual host
            tracing (bool): If true enable tracing.

        Raises:
            ApiError: If the operation fails
        """
        data = {
            'tracing': tracing
        }
        response = await self._requester.put('vhost', vhost, data=data)
        if response is not None:
            raise ApiError

    async def delete_vhost(self, vhost: str) -> None:
        """Delete an individual virtual host

        Args:
            vhost (str): The virtual host

        Raises:
            ApiError: If the operation fails
        """
        response = await self._requester.delete('vhost', vhost)
        if response is not None:
            raise ApiError

    async def get_vhost_permissions(self, name: str) -> List[Mapping[str, Any]]:
        """A list of all permissions for a given virtual host.

        Args:
            vhost (str): The virtual host

        Raises:
            ApiError: If the operation fails

        Returns:
        List[Mapping[str, Any]]: A list of permissions
        """
        response = await self._requester.get('vhosts', name, 'permissions')
        if response is None:
            raise ApiError
        return response

    async def get_vhost_topic_permissions(self, name: str) -> List[Mapping[str, Any]]:
        """A list of all topic permissions for a given virtual host.

        Args:
            vhost (str): The virtual host

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of topic permissions
        """
        response = await self._requester.get('vhosts', name, 'topic-permissions')
        if response is None:
            raise ApiError
        return response

    async def get_users(self) -> List[Mapping[str, Any]]:
        """A list of all users.

        Raises:
            ApiError: If the operation fails

        Returns:
            List[Mapping[str, Any]]: A list of users
        """
        response = await self._requester.get_list('users')
        if response is None:
            raise ApiError
        return response


"""
GET	PUT	DELETE	POST	Path	Description
X	/api/vhosts/name/start/node	Starts virtual host name on node node.
X				/api/users/without-permissions	A list of users that do not have access to any virtual host.
X	/api/users/bulk-delete	Bulk deletes a list of users. Request body must contain the list:
{"users" : ["user1", "user2", "user3"]}
X	X	X		/api/users/name	An individual user. To PUT a user, you will need a body looking something like this:
{"password":"secret","tags":"administrator"}
or:
{"password_hash":"2lmoth8l4H0DViLaK9Fxi6l9ds8=", "tags":"administrator"}
The tags key is mandatory. Either password or password_hash must be set. Setting password_hash to "" will ensure the user cannot use a password to log in. tags is a comma-separated list of tags for the user. Currently recognised tags are administrator, monitoring and management. password_hash must be generated using the algorithm described here.
X				/api/users/user/permissions	A list of all permissions for a given user.
X				/api/users/user/topic-permissions	A list of all topic permissions for a given user.
X				/api/whoami	Details of the currently authenticated user.
X				/api/permissions	A list of all permissions for all users.
X	X	X		/api/permissions/vhost/user	An individual permission of a user and virtual host. To PUT a permission, you will need a body looking something like this:
{"configure":".*","write":".*","read":".*"}
All keys are mandatory.
X				/api/topic-permissions	A list of all topic permissions for all users.
X	X	X		/api/topic-permissions/vhost/user	Topic permissions for a user and virtual host. To PUT a topic permission, you will need a body looking something like this:
{"exchange":"amq.topic","write":"^a","read":".*"}
All keys are mandatory.
X				/api/parameters	A list of all vhost-scoped parameters.
X				/api/parameters/component	A list of all vhost-scoped parameters for a given component.
X				/api/parameters/component/vhost	A list of all vhost-scoped parameters for a given component and virtual host.
X	X	X		/api/parameters/component/vhost/name	An individual vhost-scoped parameter. To PUT a parameter, you will need a body looking something like this:
{"vhost": "/","component":"federation","name":"local_username","value":"guest"}
X				/api/global-parameters	A list of all global parameters.
X	X	X		/api/global-parameters/name	An individual global parameter. To PUT a parameter, you will need a body looking something like this:
{"name":"user_vhost_mapping","value":{"guest":"/","rabbit":"warren"}}
X				/api/policies	A list of all policies.
X				/api/policies/vhost	A list of all policies in a given virtual host.
X	X	X		/api/policies/vhost/name	An individual policy. To PUT a policy, you will need a body looking something like this:
{"pattern":"^amq.", "definition": {"federation-upstream-set":"all"}, "priority":0, "apply-to": "all"}
pattern and definition are mandatory, priority and apply-to are optional.
X				/api/operator-policies	A list of all operator policiy overrides.
X				/api/operator-policies/vhost	A list of all operator policiy overrides in a given virtual host.
X	X	X		/api/operator-policies/vhost/name	An individual operator policy. To PUT a policy, you will need a body looking something like this:
{"pattern":"^amq.", "definition": {"expires":100}, "priority":0, "apply-to": "queues"}
pattern and definition are mandatory, priority and apply-to are optional.
X				/api/aliveness-test/vhost	Declares a test queue, then publishes and consumes a message. Intended for use by monitoring tools. If everything is working correctly, will return HTTP status 200 with body:
{"status":"ok"}
Note: the test queue will not be deleted (to to prevent queue churn if this is repeatedly pinged).
X				/api/healthchecks/node	Runs basic healthchecks in the current node. Checks that the rabbit application is running, channels and queues can be listed successfully, and that no alarms are in effect. If everything is working correctly, will return HTTP status 200 with body:
{"status":"ok"}
If something fails, will return HTTP status 200 with the body of
{"status":"failed","reason":"string"}
X				/api/healthchecks/node/node	Runs basic healthchecks in the given node. Checks that the rabbit application is running, list_channels and list_queues return, and that no alarms are raised. If everything is working correctly, will return HTTP status 200 with body:
{"status":"ok"}
If something fails, will return HTTP status 200 with the body of
{"status":"failed","reason":"string"}
X				/api/vhost-limits	Lists per-vhost limits for all vhosts.
X				/api/vhost-limits/vhost	Lists per-vhost limits for specific vhost.
X	X		/api/vhost-limits/vhost/name	Set or delete per-vost limit for vhost with name. Limits are set using a JSON document in the body:
{"max-connections": 100, "max-queues": 200}
"""
