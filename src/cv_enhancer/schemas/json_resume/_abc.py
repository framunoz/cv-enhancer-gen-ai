import abc
import typing as t

from pydantic import BaseModel
from pydantic._internal import _model_construction


class JsonResumeBaseModel(BaseModel, metaclass=_model_construction.ModelMetaclass):
    """Base class for JSON Resume models."""

    __EXAMPLE__: t.ClassVar

    @abc.abstractmethod
    def get_id(self) -> str:
        """Returns a unique identifier for the model instance."""
        ...

    @property
    @abc.abstractmethod
    def item_type(self) -> str:
        """Returns the type of the item represented by the model."""
        ...

    @property
    def has_keywords(self) -> bool:
        """Indicates whether the model has keywords."""
        return hasattr(self, "keywords") and bool(getattr(self, "keywords", None))


class JsonResumeFormattableBaseModel(
    JsonResumeBaseModel, metaclass=_model_construction.ModelMetaclass
):
    """Base class for JSON Resume models that are formattable."""

    @abc.abstractmethod
    def format(self) -> str:
        """Returns a formatted string representation of the model."""
        ...
