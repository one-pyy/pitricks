import logging
from rich.logging import RichHandler

__all__ = ['init_log']

def init_log(level, filename: str = ""):
  """自用初始化log"""
  logging.root.setLevel(logging.NOTSET)
  
  if filename:
    file_formatter = logging.Formatter(
      fmt='%(asctime)s [%(levelname)s] %(pathname)s,%(lineno)d:%(funcName)s    %(message)s',
      datefmt="%Y-%m-%d %H:%M:%S")
    file_handler = logging.FileHandler(filename, encoding='UTF-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    logging.root.addHandler(file_handler)
  
  rich_formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s] %(pathname)s,%(lineno)d: %(funcName)s\n%(message)s',
    datefmt="%H:%M:%S")
  rich = RichHandler(level=level,
                     show_level=False,
                     show_time=False,
                     locals_max_string=None,
                     show_path=False,
                     rich_tracebacks=True,
                     tracebacks_show_locals=True)
  rich.setFormatter(rich_formatter)
  logging.root.addHandler(rich)
