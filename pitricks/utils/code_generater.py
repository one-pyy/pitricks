from typing import Protocol

__all__ = ['CodeGenerater']

class IO(Protocol):
  def write(self, s: str, /) -> int: ...

class CodeGenerater:
  '''便于输出代码的缩进'''
  def __init__(self, io: IO, indent: int = 0, space_per_tab: int = 2):
    self.io = io
    self.indent = indent
    self.spt = space_per_tab
    self.stack: list[int] = []
  
  @property
  def indent(self):
    return self._indent
  
  @indent.setter
  def indent(self, value: int):
    assert value>=0, '缩进不能为负数'
    self._indent = value
  
  def __int__(self):
    return self.indent
  
  def __str__(self) -> str:
    return ' '*self.indent
  
  def push(self):
    self.stack.append(self.indent)
    return self
  
  def pop(self):
    self.indent = self.stack.pop()
    return self
  
  def add(self, n: int = 1):
    self.indent += n*self.spt
    return self
  
  def sub(self, n: int = 1):
    self.indent -= n*self.spt
    return self
  
  def write(self, s: str):
    self.io.write(str(self))
    self.io.write(s)
    self.io.write('\n')
    return self

