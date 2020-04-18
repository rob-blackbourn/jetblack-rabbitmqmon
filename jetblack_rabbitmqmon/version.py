from __future__ import annotations
from typing import Optional, Iterable, Tuple


def _zip(
        v1: List[int, ...],
        v2: Tuple[int, ...],
        fillvalue1: Optional[int],
        fillvalue2: Optional[int]
) -> Iterable[Tuple[int, int]]:
    l1, l2 = len(v1), len(v2)
    if fillvalue1 is not None and l1 < l2:
        v1 = list(v1) + [fillvalue1] * (l2 - l1)
    if fillvalue2 is not None and l2 < l1:
        v2 = list(v2) + [fillvalue2] * (l1 - l2)
    return zip(v1, v2)


class Version:
    """The RabbitMQ version"""

    def __init__(self, version: str, fillvalue: Optional[int] = None) -> None:
        """The RabbitMQ version

        Args:
            version (str): The versionn string
            fillvalue (Optional[int], optional): The fill value. Defaults to None.
        """
        self.version = version
        self.version_tuple = tuple(int(i) for i in version.split('.'))
        self.fillvalue = fillvalue

    def __str__(self) -> str:
        return self.version

    __repr__ = __str__

    def _compare(self, other: Version) -> int:
        for a, b in _zip(self.version_tuple, other.version_tuple, self.fillvalue, other.fillvalue):
            if a > b:
                return 1
            elif a < b:
                return -1
        return 0

    def __eq__(self, other) -> bool:
        return self._compare(other) == 0

    def __ne__(self, other) -> bool:
        return self._compare(other) != 0

    def __lt__(self, other) -> bool:
        return self._compare(other) < 0

    def __le__(self, other) -> bool:
        return self._compare(other) <= 0

    def __gt__(self, other) -> bool:
        return self._compare(other) > 0

    def __ge__(self, other) -> bool:
        return self._compare(other) >= 0
