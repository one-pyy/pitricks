import asyncio as ai
from typing import *

def run_sync(async_func: Union[Awaitable, Iterable[Awaitable]]):
  """以同步的方式运行异步函数, 可能需要先patch"""
  if isinstance(async_func, Iterable):
    async def run_gather():
      return await ai.gather(*async_func)
    async_func = run_gather()
  loop = ai.get_event_loop()
  return loop.run_until_complete(async_func)


def patch_asyncio():
  """解决协程循环不能重复创建"""
  import nest_asyncio
  nest_asyncio.apply()
