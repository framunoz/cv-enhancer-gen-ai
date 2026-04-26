import typing as t
from threading import Lock


class _SingletonMeta(type):
    """A thread-safe implementation of Singleton.

    Use this metaclass to create singleton classes.

    Example:
        class MySingleton(metaclass=_SingletonMeta):
            pass

        instance1 = MySingleton()
        instance2 = MySingleton()
        assert instance1 is instance2
    """

    _instances: dict[type, t.Any] = {}  # noqa: RUF012
    _lock: Lock = Lock()

    def __call__(cls, *args: t.Any, **kwargs: t.Any) -> t.Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
