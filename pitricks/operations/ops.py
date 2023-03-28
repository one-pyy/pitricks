"没写()"
import base64
import binascii
import datetime
import functools
import hashlib
import html
import json
import re
import struct
import time
import urllib.parse
from typing import *

T1 = TypeVar("T1")
T2 = TypeVar("T2")

class Operation(Generic[T1, T2]):
  def __init__(self,
               ror_func: Callable[..., T2] = lambda x: x):
    self.ror_func = ror_func
  
  def __ror__(self, left: T1) -> T2:
    return self.ror_func(left)

def to_bytes(func):
  @functools.wraps(func)
  def wrapper(x, *args, **kwargs):
    if type(x) == str:
      coding = kwargs.get('encoding', None)
      x = x.encode(encoding=coding)
      kwargs.pop('encoding', None)
    return func(x, *args, **kwargs)
  return wrapper


def to_str(func):
  @functools.wraps(func)
  def wrapper(x, *args, **kwargs):
    if type(x) == bytes:
      coding = kwargs.get('encoding', None)
      x = x.decode(encoding=coding)
      kwargs.pop('encoding', None)
    return func(x, *args, **kwargs)
  return wrapper
...
...
...