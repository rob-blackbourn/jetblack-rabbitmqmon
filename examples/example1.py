"""Example"""

import asyncio
import os

from jetblack_rabbitmqmon.monitor import Monitor, Requester
from jetblack_rabbitmqmon.clients.httpx_requester import HttpxRequester
from jetblack_rabbitmqmon.clients.aiohttp_requester import AioHttpRequester


async def main_async(requester: Requester) -> None:
    mon = Monitor(requester)

    overview = await mon.overview()
    print(overview)

    version = await mon.management_version()
    print(version)

    cluster_name = await mon.cluster_name()
    print(cluster_name)

    extensions = await mon.extensions()
    print(extensions)

    definitions = await mon.definitions()
    print(definitions)

    vhosts = await mon.vhosts()
    print(vhosts)

    vhost = vhosts['/prd']
    exchanges = await vhost.exchanges()
    for exchange in exchanges.values():
        print(exchange)
        await exchange.refresh()
        print(exchange)
        bindings = await exchange.bindings()
        for binding in bindings:
            print(binding)

    queues = await vhost.queues()
    for queue in queues.values():
        print(queue)
        await queue.refresh()
        print(queue)
        bindings = await queue.bindings()
        for binding in bindings:
            print(binding)
            props = await binding.props()
            print(props)

    channels = await mon.channels()
    for channel in channels:
        print(channel)
        await channel.refresh()
        print(channel)

    connections = await mon.connections()
    for connection in connections:
        print(connection)
        await connection.refresh()
        print(connection)

    users = await mon.users()
    for user in users:
        print(user)

    nodes = await mon.nodes()
    print(nodes)
    for node in nodes:
        print(node)
        await node.refresh(True, True)
        print(node)

if __name__ == '__main__':
    aiohttp_requester = AioHttpRequester(
        os.environ['RABBITMQ_URL'],
        os.environ['RABBITMQ_USERNAME'],
        os.environ['RABBITMQ_PASSWORD']
    )
    httpx_requester = HttpxRequester(
        os.environ['RABBITMQ_URL'],
        os.environ['RABBITMQ_USERNAME'],
        os.environ['RABBITMQ_PASSWORD']
    )

    asyncio.run(main_async(aiohttp_requester))
