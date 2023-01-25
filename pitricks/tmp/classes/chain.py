try:
  from ...utils.reflect import get_args
except:
  from pitricks.utils.reflect import get_args

# auto generate FileHandler
from logging import FileHandler

class FileHandler_(FileHandler):
  def close(self):
    args, kwargs = get_args(super().close)
    super().close(*args, **kwargs)
    return self

  def emit(self, record):
    args, kwargs = get_args(super().emit)
    super().emit(*args, **kwargs)
    return self

  def flush(self):
    args, kwargs = get_args(super().flush)
    super().flush(*args, **kwargs)
    return self

  def set_name(self, name):
    args, kwargs = get_args(super().set_name)
    super().set_name(*args, **kwargs)
    return self

  def createLock(self):
    args, kwargs = get_args(super().createLock)
    super().createLock(*args, **kwargs)
    return self

  def acquire(self):
    args, kwargs = get_args(super().acquire)
    super().acquire(*args, **kwargs)
    return self

  def release(self):
    args, kwargs = get_args(super().release)
    super().release(*args, **kwargs)
    return self

  def setLevel(self, level):
    args, kwargs = get_args(super().setLevel)
    super().setLevel(*args, **kwargs)
    return self

  def setFormatter(self, fmt):
    args, kwargs = get_args(super().setFormatter)
    super().setFormatter(*args, **kwargs)
    return self

  def handleError(self, record):
    args, kwargs = get_args(super().handleError)
    super().handleError(*args, **kwargs)
    return self

  def addFilter(self, filter):
    args, kwargs = get_args(super().addFilter)
    super().addFilter(*args, **kwargs)
    return self

  def removeFilter(self, filter):
    args, kwargs = get_args(super().removeFilter)
    super().removeFilter(*args, **kwargs)
    return self

# auto generate Thread
from threading import Thread

class Thread_(Thread):
  def start(self):
    args, kwargs = get_args(super().start)
    super().start(*args, **kwargs)
    return self

  def run(self):
    args, kwargs = get_args(super().run)
    super().run(*args, **kwargs)
    return self

  def join(self, timeout=None):
    args, kwargs = get_args(super().join)
    super().join(*args, **kwargs)
    return self

  def setDaemon(self, daemonic):
    args, kwargs = get_args(super().setDaemon)
    super().setDaemon(*args, **kwargs)
    return self

  def setName(self, name):
    args, kwargs = get_args(super().setName)
    super().setName(*args, **kwargs)
    return self

