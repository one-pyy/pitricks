from typing import *
import inspect
import logging
import ast
import io

import regex as re

from ...utils.code_generater import CodeGenerater
from ...path import TMP_CLASS_PATH

T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')

class BuiltinFuncExp(Exception): pass

def _del_indent(source: str):
  """删除代码缩进"""
  lines = source.expandtabs().split('\n')
  indent = min(len(line) - len(line.lstrip()) for line in lines if line != '')
  return '\n'.join(line[indent:] for line in lines)

def _has_return(func: Callable):
  '使用ast语法树判断函数是否仅返回None'
  try:
    source = inspect.getsource(func)
  except TypeError:
    logging.warning(f'函数{func.__name__}不是python函数，无法判断是否有返回值(已忽略)')
  else:
    tree = ast.parse(_del_indent(source))
    for node in ast.walk(tree):
      if isinstance(node, (ast.Yield, ast.YieldFrom)):
        return True
      if isinstance(node, ast.Return):
        v = node.value
        # 当return None时跳过
        if not (v is None or (isinstance(v, ast.Constant) and v.value is None)):
          return True
  return False

# def _filter(dic: Mapping[T1, T2], func: Callable[[T1, T2], bool]):
#   return {k: v for k, v in dic.items() if func(k, v)}

def _all_attr(cls: type)->Mapping[str, Any]:
  ret = {}
  for c in cls.mro():
    ret.update(c.__dict__)
  return ret

def _no_ret_api(dic: Mapping[str, T]):
  "去除私有方法、魔术方法、可能返回值的函数、生成器、非函数"
  return {k:v for k,v in dic.items() if not k.startswith('_') and isinstance(v, Callable) and not _has_return(v)}

def _func_info(func: Callable):
  """获取函数定义，如：def func(a, b, c=1, d=2)"""
  try:
    source = inspect.getsource(func)
  except TypeError:
    logging.critical(f'这是未知的问题')
  else:
    #获取以def开头的部分
    source = _del_indent(source)
    lines = source.split('\n')
    while not lines[0].startswith('def'):
      lines.pop(0)
    source = '\n'.join(lines)
    
    #以括号为界限，获取函数定义到右括号
    bracket = 0
    for i, c in enumerate(source):
      if c == '(':
        bracket += 1
      elif c == ')':
        bracket -= 1
        if bracket == 0:
          while source[i] != ':':
            # 应该没有人会写literal[":"], 先略过吧
            i += 1
          return source[:i+1]
  
  raise Exception("It looks like there is a bug, please submit an issue.")

def chain(cls: Union[type, Iterable[type]], expect_func_name: list[str] = []) -> str:
  """使传入类可以链式调用，即每个方法返回self;
  expect_func_name用于指定不需要链式调用的方法名，双下划线开头的魔术方法已经自动省略;
  会返回创建类的代码, 同时写入tmp_class, 可以from pitricks.tmp_class import xxx;"""
  
  if isinstance(cls, Iterable):
    ret = []
    for c in cls:
      ret.append(chain(c, expect_func_name))
    return '\n'.join(ret)
  
  assert isinstance(cls, type), '传入的参数必须是类'
    
  target_funcs = _no_ret_api(
    {k:v for k,v in _all_attr(cls).items() if k not in expect_func_name})
  
  ios = io.StringIO()
  code = CodeGenerater(ios)
  # import
  if not open(TMP_CLASS_PATH/'__init__.py').read():
    code.write(f'try:').add() \
        .write(f'from ...utils.reflect import get_args').sub() \
        .write(f'except:').add() \
        .write(f'from pitricks.utils.reflect import get_args\n').sub()
  
  code.write(f'# auto generate {cls.__name__}') \
      .write(f'from {cls.__module__} import {cls.__name__}\n')
  # class
  code.write(f'class {cls.__name__}_({cls.__name__}):').add()
  
  # func
  for func_name, func in target_funcs.items():
    # def
    func_def = re.sub(r'(?<=def\s+)[\w_]+', func_name, _func_info(func))
    code.write(func_def).push().add()
    
    # func_body
    code.write(f'args, kwargs = get_args(super().{func_name})') \
        .write(f'super().{func_name}(*args, **kwargs)') \
        .write(f'return self\n').pop()
  
  open(TMP_CLASS_PATH/'chain.py', 'a').write(code.io.getvalue()) # type: ignore
  open(TMP_CLASS_PATH/'__init__.py', 'a').write(
    f'from .chain import {cls.__name__}_ as {cls.__name__}\n')
  
  return code.io.getvalue() # type: ignore

def clear_tmp_code():
  open(TMP_CLASS_PATH/'chain.py', 'w')
  open(TMP_CLASS_PATH/'__init__.py', 'w')