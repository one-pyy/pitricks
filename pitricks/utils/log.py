import logging as lg
from rich.logging import RichHandler

__all__ = ['init_log']

def init_log(level, filename: str = ""):
  """自用初始化log"""
  lg.root.setLevel(lg.NOTSET)
  
  if filename:
    file_formatter = lg.Formatter(
      fmt='%(asctime)s [%(levelname)s] %(pathname)s,%(lineno)d: %(funcName)s\n\t%(message)s',
      datefmt="%Y-%m-%d %H:%M:%S")
    file_handler = lg.FileHandler(filename, encoding='UTF-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    lg.root.addHandler(file_handler)
  
  rich_formatter = lg.Formatter(
    fmt='%(asctime)s [%(levelname)s] %(pathname)s,%(lineno)d: %(funcName)s\n\t%(message)s',
    datefmt="%H:%M:%S")
  rich = RichHandler(level=level,
                     show_level=False,
                     show_time=False,
                     locals_max_string=None, # type: ignore
                     show_path=False,
                     rich_tracebacks=True,
                     tracebacks_show_locals=True)
  rich.setFormatter(rich_formatter)
  lg.root.addHandler(rich)
