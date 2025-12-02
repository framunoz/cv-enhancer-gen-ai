import abc
import typing as t

from pydantic import BaseModel
from pydantic._internal import _model_construction


class JsonResumeBaseModel(BaseModel, metaclass=_model_construction.ModelMetaclass):
    """Base class for JSON Resume models."""

    @abc.abstractmethod
    def format(self) -> str:
        """Returns a formatted string representation of the model."""
        ...

    @abc.abstractmethod
    def get_id(self) -> str:
        """Returns a unique identifier for the model instance."""
        ...

    @property
    @abc.abstractmethod
    def item_type(self) -> str:
        """Returns the type of the item represented by the model."""
        ...
