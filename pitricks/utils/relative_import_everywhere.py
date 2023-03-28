"""from https://gist.github.com/vaultah/d63cb4c86be2774377aa674b009f759a"""
import sys
import importlib
from pathlib import Path

def make_parent_top(level=1):
  """Import parent module(s) so that relative imports work. 
  Will auto check if the '__name__' of caller is '__main__' and '__package__' is None."""
  caller_var = sys._getframe(1).f_globals

  if caller_var['__name__'] != '__main__' or caller_var['__package__'] is not None:
    return
  
  file = Path(caller_var['__file__']).resolve()
  parent, top = file.parent, file.parents[level]
  sys.path.append(str(top))
  try:
    sys.path.remove(str(parent))
  except ValueError: # already removed
    pass
  package = caller_var['__package__'] = '.'.join(parent.parts[len(top.parts):])
  importlib.import_module(package) # won't be needed after that


if __name__ == '__main__' and __package__ is None:
  make_parent_top(level=2)
  from . import reflect
  print(reflect)