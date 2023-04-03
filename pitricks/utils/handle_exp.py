"让函数只抛出未知异常"
import logging
import re
import traceback
from typing import Callable, Optional, Union, Coroutine, Any

from .types import *

__all__ = ['catch_exp', 'acatch_exp']

def _handle_exp(e: Exception,
                echo,
                log_level,
                raise_exp,
                catch_regex):
  if raise_exp:
    raise

  if catch_regex != ".*":
    info = str(e)
    if not re.search(catch_regex, info):
      raise

  if echo:
    traceback.print_exc()
  
  if log_level!=-1:
    logging.log(log_level, traceback.format_exc())


def catch_exp(func: Callable[..., T1], 
              *args, 
              _echo=False,
              _log_level=-1,
              _raise_exp=False,
              _catch_classes: Exps = Exception,
              _catch_regex: Union[str, re.Pattern] = ".*",
              _failed_return: Optional[T2] = None,
              **kwargs) -> Union[T1, Optional[T2]]:
  """执行func函数, 参数给args和kwargs, 如果发生异常, 则根据其他参数处理异常
  如果log_level为-1, 则不记录日志, 否则记录日志, 且日志级别为log_level; 可以传入logging.DEBUG等常量"""
  if not isinstance(_catch_classes, tuple):
    _catch_classes = (_catch_classes, )

  try:
    return func(*args, **kwargs)
  except _catch_classes as e:
    _handle_exp(e, _echo, _log_level, _raise_exp, _catch_regex)
    return _failed_return


async def acatch_exp(coroutine: Coroutine[Any, Any, T],
                     echo=False,
                     log_level=-1,
                     raise_exp=False,
                     catch_classes: Exps = Exception,
                     catch_regex: Union[str, re.Pattern] = ".*",
                     failed_return: Optional[T2] = None) -> Union[T, Optional[T2]]:
  """(async版)执行传入的coroutine, 如果发生异常, 则根据其他参数处理异常
  如果log_level为-1, 则不记录日志, 否则记录日志, 且日志级别为log_level; 可以传入logging.DEBUG等常量"""
  if not isinstance(catch_classes, tuple):
    catch_classes = (catch_classes, )

  try:
    return await coroutine
  except catch_classes as e:
    _handle_exp(e, echo, log_level, raise_exp, catch_regex)
    return failed_return


