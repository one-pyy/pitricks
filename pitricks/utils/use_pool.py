"Automatically add the operation of pooling when the object is destructed"
from typing import *
from queue import Queue, Empty

T = TypeVar('T')
T1 = TypeVar('T1')

class PoolProtocol(Protocol[T]):
  "Of course you can add more parameters to the get methods without reporting an error"
  def put(self, obj: T, /): ...
  def get_or_none(self) -> Union[T, None]: ...

class ExamplePool(Generic[T]):
  def __init__(self) -> None:
    super().__init__()
    self.q = Queue()
  
  def put(self, obj: T):
    self.q.put(obj)
  
  def get_or_none(self) -> Union[T, None]:
    try:
      return self.q.get_nowait()
    except Empty:
      return None

def use_pool(Tp: Type[T], 
             pool: Optional[PoolProtocol[T1]] = None) -> Type[T]:
  "请自行在__init__中检测是否需要重新初始化实例"
  pool: PoolProtocol[T1] = pool or ExamplePool()
  class NewTp:
    def __new__(cls, *args, **kwargs):
      obj = pool.get_or_none()
      if obj is None:
        obj = object.__new__(Tp, *args, **kwargs)
      new_tp = super().__new__(cls)
      object.__setattr__(new_tp, 'me', obj)
      return new_tp
    
    def __init__(self, *args, **kwargs):
      super().__init__()
      super().__getattribute__('me').__init__(*args, **kwargs)
    
    def __del__(self):
      pool.put(super().__getattribute__('me'))
    
    def __getattribute__(self, name: str):
      if name not in ('__new__', '__init__', '__del__'):
        return super().__getattribute__('me').__getattribute__(name)
  
  return NewTp # type: ignore

if __name__=='__main__':
  class Test:
    def __init__(self, a):
      if getattr(self, 'a', None) != a:
        self.a = a 
        print(f'init! a={self.a}; id={id(self)}')
      else:
        print(f'pooled! a={self.a}; id={id(self)}')
    def p(self):
      print(self.a)
    def __del__(self):
      print(f'del! id={id(self)}')
  
  PooledTest = use_pool(Test, ExamplePool())
  a = PooledTest(1)
  del a
  b = PooledTest(1)
  del b
  c = PooledTest(1)
  del c
  d = PooledTest(2)
  e = PooledTest(2)
  del d
  del e
  f = PooledTest(2)
  f.p()
  del f
  