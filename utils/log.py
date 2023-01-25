import logging

__all__ = ['init_log']

def init_log(filename: str = ""):
  """自用初始化log"""
  logging.root.setLevel(logging.NOTSET)
  formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s] %(filename)s,%(lineno)d:%(funcName)s    %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")
  
  if filename:
    file_handler = logging.FileHandler(filename, encoding='UTF-8')
    file_handler.setFormatter(formatter)
    logging.root.addHandler(file_handler)
  
  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(formatter)
  logging.root.addHandler(stream_handler)
