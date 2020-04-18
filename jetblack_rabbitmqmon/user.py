"""User"""

from .api import Api


class User:
    """A RabbitMQ user"""

    def __init__(
            self,
            api: Api,
            name: str,
            password_hash: str,
            hashing_algorithm: str,
            tags: str
    ):
        """A RabbitMQ user

        Args:
            api (Api): The api
            name (str): The user name
            password_hash (str): The password hash
            hashing_algorithm (str): The hashing algorithm
            tags (str): The tags

        Attributes:
            name (str): The user name
            password_hash (str): The password hash
            hashing_algorithm (str): The hashing algorithm
            tags (str): The tags
        """
        self.api = api
        self.name = name
        self.password_hash = password_hash
        self.hashing_algorithm = hashing_algorithm
        self.tags = tags

    def __str__(self) -> str:
        return '<User {name}>'.format(
            name=self.name
        )

    def __repr__(self) -> str:
        return str(self)
