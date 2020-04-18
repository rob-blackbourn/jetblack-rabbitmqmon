# jetblack-rabbitmqmon

This is an asyncio RabbitMQ monitor API.

It wraps the RabbitMQ management plugin REST api. This allows retrieving
metrics and peeking into the queues.

## Status

This is work in progress, but is functional.

## Installation

This can be installed with pip.

Multiple clients a supported and one *must* be selected. Choose one of:

* [aiohttp](https://github.com/aio-libs/aiohttp)
* [bareclient](https://github.com/rob-blackbourn/bareClient)

```bash
pip install jetblack-rabbitmqmon[bareclient]
```

Or alternatively:

```bash
pip install jetblack-rabbitmqmon[aiohttp]
```


## Usage

The following gets an overview using the bareclient.

```python
import asyncio
from jetblack_rabbitmqmon.monitor import Monitor
from jetblack_rabbitmqmon.clients.bareclient_requester import BareRequester

async def main_async():
    mon = Monitor(
        BareRequester(
            'http://mq.example.com:15672',
            'admin',
            'admins password'
        )
    )

    overview = await mon.overview()
    print(overview)

if __name__ == '__main__':
    asyncio.run(main_async())
```

The follow explores a vhost.

```python
import asyncio
from jetblack_rabbitmqmon.monitor import Monitor
from jetblack_rabbitmqmon.clients.aiohttp_requester import AioHttpRequester

async def main_async():
    mon = Monitor(
        AioHttpRequester(
            'http://mq.example.com:15672',
            'admin',
            'admins password'
        )
    )

    vhosts = await mon.vhosts()
    for vhost in vhosts.values(): # vhost is a dict
      exchanges = await vhost.exchanges()
      for exchange in exchanges.values(): # exchanges is a dict
          print(exchange)
          # Objects can be refreshed to gather new metrics.
          await exchange.refresh()
          print(exchange)
          bindings = await exchange.bindings()
          for binding in bindings:
              print(binding)

if __name__ == '__main__':
    asyncio.run(main_async())
```

The following gets some messages from an exchange:

```python
import asyncio
from jetblack_rabbitmqmon.monitor import Monitor
from jetblack_rabbitmqmon.clients.bareclient_requester import BareRequester

async def main_async():
    mon = Monitor(
        BareRequester(
            'http://mq.example.com:15672',
            'admin',
            'admins password'
        )
    )

    vhosts = await mon.vhosts()
    vhost = vhosts['/some-vhost']
    queues = await vhost.queues()
    queue = queues['some.queue']
    messages = await queue.get_messages()
    print(messages)

if __name__ == '__main__':
    asyncio.run(main_async())
```

