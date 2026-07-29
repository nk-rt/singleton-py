from typing import Any

class _SingletonWrapper[cls_T]:
    """
    Enforces a singleton pattern by caching and returning a single class instance. Adheres to 
    PEP 695 [1] (type parameter syntax) and PEP 8 [2] (structural style guidelines).

    References
    ----------
    [1] https://peps.python.org/pep-0695/
    [2] https://peps.python.org/pep-0008/
    """

    def __init__(self, cls: type[cls_T]) -> None:
        self.__wrapped__: type[cls_T] = cls
        self._instance: cls_T | None = None

    def __call__(self, *args: Any, **kwargs: Any) -> cls_T:
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)
        return self._instance
    
    def __getattr__(self, name: str) -> Any:
        return getattr(self.__wrapped__, name)
    

def singleton[func_T](cls: type[func_T]) -> _SingletonWrapper[func_T]:
    """
    A singleton decorator. Returns a wrapper object. Wraps a target class to manage its global
    instantiation state.
    """
    return _SingletonWrapper(cls)
