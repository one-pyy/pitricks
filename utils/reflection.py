from typing import *
import sys

def get_upper_kwargs(level=1) -> dict[str, Any]:
  """获取上x层的变量, 但只是浅拷贝"""
  return sys._getframe(level+1).f_locals


def kwargs_to_dict() -> dict[str, Any]:
  """获取本层传入了什么, 于是你可以把它传给下一层"""
  kwargs = get_upper_kwargs(0)
  return kwargs
