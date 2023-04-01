from typing import Any, Callable
from pathlib import Path
import sys
import inspect

__all__ = ['get_upper_vars', 'get_args', 'pwd']

def get_upper_vars(level: int = 1, with_global: bool = False) -> 'dict[str, Any]':
  """获取上x层的变量, 但只是浅拷贝"""
  last_frame = sys._getframe(level+1)
  if with_global:
    return dict(last_frame.f_locals, **last_frame.f_globals)
  else:
    return last_frame.f_locals


def get_args(func: Callable, del_self: bool = True) -> 'tuple[list, dict[str, Any]]':
  """当你在一个函数上套另一层时, 可能需要将参数无损传递..."""
  upper_vars = get_upper_vars()
  paras = dict(inspect.signature(func).parameters)
  if del_self:
    paras.pop('self', None)
  
  args = []
  kwargs: 'dict[str, Any]' = {}
  need_keyword = False #当出现了VAR_POSITIONAL后位置参数就要转为关键字参数了
  
  for name, para in paras.items():
    try:
      var = upper_vars[name]
    except KeyError:
      raise Exception("或许我们需要复制你试图wrap的这个函数的参数...")
    else:
      
      if para.kind==para.POSITIONAL_ONLY:
        args.append(var)
      elif para.kind==para.VAR_POSITIONAL:
        args.extend(var)
        need_keyword = True
      elif para.kind==para.VAR_KEYWORD:
        kwargs.update(var)
      elif need_keyword:
        kwargs[name] = var
      else:
        args.append(var)
        
  return args, kwargs


def pwd() -> Path:
  """获取当前文件所在文件夹的绝对路径"""
  path = get_upper_vars(with_global=True)['__file__']
  return Path(path).parent

if __name__=='__main__':
  def k(d, /, b=1, *args, c=3, **kwargs):
    pass
  
  def q(d, /, b=1, *args, c=3, **kwargs):
    args, kwargs = get_args(k)
    print(args, kwargs) # [1, 2, 3] {'c': 4, 'd': 5, 'e': 6, 'f': 7}
    return k(*args, **kwargs)
  
  q(1, 2, 3, c=4, d=5, e=6, f=7)