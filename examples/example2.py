"""Example"""

import asyncio
import os

from jetblack_rabbitmqmon.monitor import Monitor, Requester
from jetblack_rabbitmqmon.clients.httpx_requester import HttpxRequester


async def main_async(requester: Requester) -> None:
    mon = Monitor(requester)

    vhosts = await mon.vhosts()
    print(vhosts)

    if 'prd' not in vhosts:
        vhost = await mon.create_vhost('prd')
    else:
        vhost = vhosts['prd']

    exchanges = await vhost.exchanges()
    if 'test_exchange' not in exchanges:
        exchange = await vhost.create_exchange(
            'test_exchange',
            'topic',
            True,
            False,
            False
        )
    else:
        exchange = exchanges['test_exchange']

    queues = await vhost.queues()
    if 'test_queue' not in queues:
        queue = await vhost.create_queue(
            'test_queue',
            True,
            False
        )
    else:
        queue = queues['test_queue']

    bindings = await queue.bindings()
    if not any(
        binding.source == exchange.name and
        binding.routing_key == 'test.#'
        for binding in bindings
    ):
        await queue.create_binding(exchange.name, 'test.#')
        bindings = await queue.bindings()

    for binding in bindings:
        if binding.source == exchange.name and binding.routing_key == 'test.#':
            await queue.delete_binding(exchange.name, binding.properties_key)

    await queue.delete()
    await exchange.delete()
    await vhost.delete()

    print('Done')

if __name__ == '__main__':
    httpx_requester = HttpxRequester(
        "http://localhost:15672",
        "guest",
        "guest"
    )

    asyncio.run(main_async(httpx_requester))
