"当函数出现已知异常时重试"
from typing import Callable, Union, overload, Optional
import re
import time
from functools import wraps
from inspect import iscoroutinefunction

from .handle_exp import acatch_exp, catch_exp
from .types import *

__all__ = ['retry', 'aretry']

def _calc_next_interval(interval: float, 
                       retry_interval: IntervalType):
  if isinstance(retry_interval, tuple):
    _, max_interval, multiplier = retry_interval
    if callable(multiplier):
      interval = multiplier(interval)
    else:
      interval += multiplier
    interval = min(interval, max_interval)
  else:
    interval = retry_interval
  return interval


@overload
def retry(func: Callable[..., T], /,
          *args, 
          _times: int = -1,
          _interval: IntervalType = 0,
          _exp: ExpType = Exception,
          _regex: Union[str, re.Pattern] = ".*",
          **kwargs) -> T: ...

@overload
def retry(*args, 
          _times: int = -1,
          _interval: IntervalType = 0,
          _exp: ExpType = Exception,
          _regex: Union[str, re.Pattern] = ".*",
          **kwargs) -> WrapperType: ...

def retry(func: Optional[Callable[..., T]] = None, /,
          *args, 
          _times: int = -1,
          _interval: IntervalType = 0,
          _exp: ExpType = Exception,
          _regex: Union[str, re.Pattern] = ".*",
          **kwargs) -> Union[T, WrapperType]:
  """重试, 可以用于装饰器, 也可以用于函数;
  _times: 重试时间, -1为无限重试; 
  _interval: 重试间隔, 可以是一个数字, 也可以是元组(最小间隔, 最大间隔, 乘数), 也可以自定义从上一个间隔计算下一个的函数; 
  _exp: 重试的异常, 可以是一个异常类, 也可以是一个异常类的元组; 
  _regex: 重试的异常信息的正则表达式, 默认为".*", 与retry_exp是`与`的关系 """
  if not isinstance(_exp, tuple):
    _exp = (_exp, )
  interval = _interval if isinstance(_interval, float) else _interval[0]
  
  if func is None:
    # 用于装饰器
    assert not args and not kwargs, "retry can't be used as wrapper with args or kwargs"
    
    if iscoroutinefunction(func):
      # async函数
      def awrapper(func: AsyncFuncType) -> AsyncFuncType:
        @wraps(func)
        async def ainner(*args, **kwargs):
          coroutine = func(*args, **kwargs)
          return aretry(coroutine, times=_times, interval=_interval, exp=_exp, regex=_regex)
        return ainner
      return awrapper
    else:
      # sync函数
      def wrapper(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def inner(*args, **kwargs):
          return retry(func, _times=_times, _interval=_interval, _exp=_exp, _regex=_regex, *args, **kwargs)
        return inner
      return wrapper
  
  while _times!=1:
    _times -= 1 #重试次数
    
    ret = catch_exp(func, _catch_classes=_exp, _catch_regex=_regex, _failed_return=ExpOccurred, *args, **kwargs)
    if ret is not ExpOccurred:
      return ret  # type: ignore    
    
    interval = _calc_next_interval(interval, _interval)
    time.sleep(interval)
  return func(*args, **kwargs)


async def aretry(coroutine: Coroutine[Any, Any, T],
          times: int = -1,
          interval: IntervalType = 0,
          exp: ExpType = Exception,
          regex: Union[str, re.Pattern] = ".*") -> T:
  """(async版)重试, 可以用于coroutine;
  times: 重试时间, -1为无限重试; 
  interval: 重试间隔, 可以是一个数字, 也可以是元组(最小间隔, 最大间隔, 乘数), 也可以自定义从上一个间隔计算下一个的函数; 
  exp: 重试的异常, 可以是一个异常类, 也可以是一个异常类的元组; 
  regex: 重试的异常信息的正则表达式, 默认为".*", 与retry_exp是`与`的关系 """
  if not isinstance(exp, tuple):
    exp = (exp, )
  interval = interval if isinstance(interval, float) else interval[0]
  
  while times!=1:
    times -= 1
    
    ret = await acatch_exp(coroutine, catch_classes=exp, catch_regex=regex, failed_return=ExpOccurred)
    if ret is not ExpOccurred:
      return ret  # type: ignore    
    
    interval = _calc_next_interval(interval, interval)
    time.sleep(interval)
  return await coroutine