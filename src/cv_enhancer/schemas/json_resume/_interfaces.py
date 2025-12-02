import typing as t


class Formatable(t.Protocol):
    def format(self) -> str:
        """Returns a formatted string representation of the item."""
        ...
