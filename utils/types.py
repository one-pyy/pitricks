from typing import TypeVar, Callable, Union, Coroutine, Any

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
WrapperType = Callable[[Callable[..., T]], Callable[..., T]]
ExpType = Union[type[Exception], tuple[type[Exception], ...]]
IntervalType = Union[float, tuple[float, float, float], tuple[float, float, Callable[[float], float]]]
AsyncFuncType = Callable[..., Coroutine[Any, Any, T]]

class ExpOccurred: pass
