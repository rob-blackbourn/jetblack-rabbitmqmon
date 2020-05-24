# Implementing a requester

A requester provides a subclass of `Requester`, overriding the `request`
method: It also takes the connection details in the `__init__` method.

```python
from gascode_rabbitmqmon.requester import Requester

class MyRequester(Requester):
    """An HTTP client"""

    def __init__(
            self,
            url: str,
            username: str,
            password: str,
            cafile: Optional[str] = '/etc/ssl/certs/ca-certificates.crt'
    ):
        """Setup the requester"""

    async def request(
            self,
            method: str,
            *args: str,
            data: Optional[Any] = None,
            params: Optional[Any] = None
    ) -> Optional[Any]:
        """Implement the HTTP request returning the result as unpacked JSON"""
```

Note the connection requires basic authentication.
