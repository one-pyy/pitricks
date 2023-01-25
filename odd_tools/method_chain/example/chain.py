from logging import FileHandler
from threading import Thread

from pitricks.odd_tools.method_chain import chain, clear_tmp_code

clear_tmp_code()
chain(FileHandler)
chain(Thread)