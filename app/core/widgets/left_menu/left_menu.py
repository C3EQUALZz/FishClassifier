from collections.abc import MutableMapping
from typing import Iterator


class LeftMenu(MutableMapping):
    def __init__(self):
        self._buttons = {}

    def __getitem__(self, key: str):
        return self._buttons[key]

    def __setitem__(self, key: str, value):
        self._buttons[key] = value

    def __delitem__(self, key: str) -> None:
        del self._buttons[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._buttons)

    def __len__(self) -> int:
        return len(self._buttons)



