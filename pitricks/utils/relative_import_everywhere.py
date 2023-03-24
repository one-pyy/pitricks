"""from https://gist.github.com/vaultah/d63cb4c86be2774377aa674b009f759a"""
import sys
import importlib
from pathlib import Path

def make_parent_top(level=1) -> str:
  """Import parent module(s) so that relative imports work. 
  Will auto check if the '__name__' of caller is '__main__' and '__package__' is None."""
  caller_var = sys._getframe(1).f_globals
  caller_name, caller_package, caller_path = caller_var['__name__'], caller_var['__package__'], caller_var['__file__']

  if caller_name != '__main__' or caller_package is not None:
    return caller_package
  
  file = Path(caller_path).resolve()
  parent, top = file.parent, file.parents[level]
  sys.path.append(str(top))
  try:
    sys.path.remove(str(parent))
  except ValueError: # already removed
    pass
  package = '.'.join(parent.parts[len(top.parts):])
  importlib.import_module(package) # won't be needed after that
  
  return package

if __name__ == '__main__' and __package__ is None:
  __package__ = make_parent_top(level=2)
  from . import reflect
  print(reflect)