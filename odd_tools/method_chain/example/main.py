import logging

# too much trouble
# You need to assign the class to a variable, and then configure it
from logging import FileHandler
file_handler = FileHandler('1', encoding='utf-8')
file_handler.setFormatter(...)
file_handler.setLevel(...)
logging.root.addHandler(file_handler)

# chain method
from pitricks.tmp.classes import FileHandler
logging.root.addHandler(
  FileHandler('1', encoding='utf-8').setFormatter(...).setLevel(...))



# original method
from threading import Thread
t = Thread(target=...)
t.setDaemon(True)
t.start()

# chain method
from pitricks.tmp.classes import Thread
Thread(target=...).setDaemon(True).start()