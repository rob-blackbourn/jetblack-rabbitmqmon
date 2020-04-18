# jetblack-rabbitmqmon

This is an asyncio RabbitMQ monitor API.

It wraps the RabbitMQ management plugin REST api.

## Status

This is work in progress, but is functional.

## Installation

This can be installed with pip.

```bash
pip install jetblack-rabbitmqmon
```

## Usage

The following gets an overview.

```python
import asyncio
from jetblack_rabbitmqmon.monitor import Monitor

async def main_async():
    mon = Monitor(
        'http://mq.example.com:15672',
        'admin',
        'admins password
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

async def main_async():
    mon = Monitor(
        'http://mq.example.com:15672',
        'admin',
        'admins password
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

async def main_async():
    mon = Monitor(
        'http://mq.example.com:15672',
        'admin',
        'admins password
    )

    vhosts = await mon.vhosts
    vhost = vhosts['/some-vhost']
    queues = await vhost.queues
    queue = queues['some.queue']
    messages = await queue.get_messages()
    print(messages)

if __name__ == '__main__':
    asyncio.run(main_async())
```

