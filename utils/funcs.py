import asyncio as ai
import logging
import random
import re
import sys
import time
import traceback
from typing import *

from .types import *

def init_log(filename: str = ""):
  logging.root.setLevel(logging.NOTSET)
  formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s] %(filename)s,%(lineno)d:%(funcName)s    %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")
  
  if filename:
    file_handler = logging.FileHandler(filename, encoding='UTF-8')
    file_handler.setFormatter(formatter)
    logging.root.addHandler(file_handler)
  
  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(formatter)
  logging.root.addHandler(stream_handler)


def get_upper_kwargs(level=1) -> Dict[str, Any]:
  """ 获取上x层的变量, 但是请不要修改它 """
  return sys._getframe(level+1).f_locals


def kwargs_to_dict() -> Dict[str, Any]:
  """ 获取本层传入了什么, 于是你可以把它传给下一层 """
  kwargs = get_upper_kwargs(0)
  return kwargs


RANDOM_DICT={
  "digit": """0123456789""",
  "lower": """abcdefghijklmnopqrstuvwxyz""",
  "upper": """ABCDEFGHIJKLMNOPQRSTUVWXYZ""",
  "letter": """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ""",
  "word": """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789""",
  "url": """-_.!~*'()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789""",
  "all": R"""!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ """,
}
def get_random_str(length=10, 
                   mode: Literal["all", "digit", "lower", "upper", "letter", "word", "url"]="all"):
  """ 生成一个指定长度的随机字符串 """
  str_list =[random.choice(RANDOM_DICT[mode]) for _ in range(length)]
  return ''.join(str_list)


def run_sync(async_func: Union[Awaitable, Iterable[Awaitable]]):
  """以同步的方式运行异步函数, 可能需要先patch"""
  if isinstance(async_func, Iterable):
    async def run_gather():
      return await ai.gather(*async_func)
    async_func = run_gather()
  loop = ai.get_event_loop()
  return loop.run_until_complete(async_func)


def patch_asyncio():
  import nest_asyncio
  nest_asyncio.apply()


def handle_exp(e: Exception,
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
              _echo=False,
              _log_level=-1,
              _raise_exp=False,
              _catch_classes: Union[type[Exception], tuple[type[Exception], ...]] = Exception,
              _catch_regex: Union[str, re.Pattern] = ".*",
              _failed_return: Optional[T2] = None,
              *args, **kwargs) -> Union[T1, Optional[T2]]:
  """如果log_level为-1, 则不记录日志, 否则记录日志, 且日志级别为log_level; 可以传入logging.DEBUG等常量"""
  if not isinstance(_catch_classes, tuple):
    _catch_classes = (_catch_classes, )

  try:
    return func(*args, **kwargs)
  except _catch_classes as e:
    handle_exp(e, _echo, _log_level, _raise_exp, _catch_regex)
    return _failed_return


async def acatch_exp(coroutine: Coroutine[Any, Any, T],
                     echo=False,
                     log_level=-1,
                     raise_exp=False,
                     catch_classes: Union[type[Exception], tuple[type[Exception], ...]] = Exception,
                     catch_regex: Union[str, re.Pattern] = ".*",
                     failed_return: Optional[T2] = None) -> Union[T, Optional[T2]]:
  """如果log_level为-1, 则不记录日志, 否则记录日志, 且日志级别为log_level; 可以传入logging.DEBUG等常量"""
  if not isinstance(catch_classes, tuple):
    catch_classes = (catch_classes, )

  try:
    return await coroutine
  except catch_classes as e:
    handle_exp(e, echo, log_level, raise_exp, catch_regex)
    return failed_return


