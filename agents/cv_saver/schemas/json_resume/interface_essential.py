import abc
import typing as t

from pydantic import BaseModel


class InterfaceEssential(t.Protocol):
    """
    Marker interface for essential components of the JSON Resume schema.
    """

    @abc.abstractmethod
    def get_essential(self) -> BaseModel:
        """
        Retrieve the essential fields of the model.

        Returns:
            BaseModel: An instance containing only the essential fields.
        """
        pass
