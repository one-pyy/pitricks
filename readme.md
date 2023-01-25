# pitricks

pitricks is a weird python module, to get `my python` handy.

## install

```
pip3 install -U git+https://github.com/one-pyy/pitricks
```

## utils

`pitricks.utils` is generally useless, except for `retry`, `reflect.get_args`.

### retry

Similar to python's `retry` module, but can be decorated with `async functions`. In addition, it can be subdivided according to the str of the exception.

This is a retry function in Python that can be used to decorate other functions or used as a standalone function. It supports various parameters such as retry times, retry intervals, retry exceptions, and retry exception message regular expressions. When retrying, you can specify the retry times, retry intervals, retry exception types, and retry exception message regular expressions. The retry interval can be a number, a tuple (minimum interval, maximum interval, multiplier), or a custom function to calculate the next interval from the previous interval. Retry exceptions can be a single exception type or a tuple of exception types. The retry exception message regular expression is used to match the exception message. If the retry times is not 1, the decorated function will be retried. If the retry times is 1 or the decorated function is executed successfully, the result of the decorated function will be returned.

To use this function, you can either use it as a decorator or call it as a standalone function.

1. Using it as a decorator:

   ```python
   from pitricks.utils.retry import retry
   
   @retry(times=3, interval=1, exp=(IOError, ValueError), regex=".*")
   def my_func():
       # some code here
   ```

   Here, the `my_func` will be retried 3 times with an interval of 1 second if either IOError or ValueError is raised `and` whose message match with the regex ".*"

2. Using it as a standalone function:

   ```python
   from pitricks.utils.retry import retry
   
   def my_func():
       # some code here
   
   retry(my_func, times=3, interval=1, exp=(IOError, ValueError), regex=".*")
   ```

   Here, the `my_func` will be retried 3 times with an interval of 1 second if either IOError or ValueError is raised and whose message match with the regex ".*"

You can also use the keyword arguments `times`, `interval`, `exp`, `regex` when calling the function.

Note:

- `times` : Number of times to retry (default -1, which means infinite retries)
- `interval` : Retry interval, can be a number or a tuple (minimum interval, maximum interval, multiplier), or tuple (minimum interval, maximum interval, function)
- `exp` : The exception(s) to retry on, can be a single exception class or a tuple of exception classes
- `regex` : The regular expression to match the exception message, default is ".*". Only exp messages that match the regex patten will be captured.

### reflect.get_args

This function `get_args` is used to get the arguments of a function and the variables in the upper scope.

`get_args` takes in two arguments:

- `func`: The function whose arguments you want to get.
- `del_self`: A boolean flag that indicates whether the `self` argument should be removed from the returned arguments. (default: True)

`get_args` returns a tuple containing two elements:

- A list of positional arguments
- A dictionary of keyword arguments

This function is useful when you need to wrap another function with another function, and you want to preserve the original function's arguments. The function will check the arguments of the passed in function `func` and match them with the variables in the upper scope, if all the required arguments are present it will return them as tuple of arguments and keyword arguments, otherwise it will raise an exception.

```python
from pitricks.utils.reflect import get_args
def k(d, /, b=1, *args, c=3, **kwargs):
  pass

def q(d, /, b=1, *args, c=3, **kwargs):
  args, kwargs = get_args(k)
  print(args, kwargs) # [1, 2, 3] {'c': 4, 'd': 5, 'e': 6, 'f': 7}
  # do something
  return k(*args, **kwargs)

q(1, 2, 3, c=4, d=5, e=6, f=7)
```

## odd_tools

### method_chaining

This is a tool that can convert class functions that `return None` to `return self`, while keeping the function signature unchanged (enabling you to use code hints).

```python
# chain.py
from logging import FileHandler
from threading import Thread

from pitricks.odd_tools.method_chain import chain, clear_tmp_code

clear_tmp_code()
chain(FileHandler)
chain(Thread)
```

After running the above code, you can import the class that you specified from `pitricks.tmp.classes`.(or `from pitricks import tmp_class`)

Like this:

```python
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
```

