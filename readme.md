# pitricks

[Readme.md in English](https://github.com/one-pyy/pitricks/blob/main/readme-en.md)

pitricks是一个奇怪的python模块，用来使`我的python`更顺手。

## 安装

```
pip3 install -U git+https://github.com/one-pyy/pitricks
or 
pip3 install pitricks
```

## 工具

`pitricks.utils`通常没有用处，除了`retry`, `reflect.get_args`, `use_pool`, `relative_import_everywhere.make_parent_top`。

### retry

类似于python的`retry`模块，但可以用`async`装饰。此外，它可以根据异常的str进行划分。

这是一个Python重试函数，可用于装饰其他函数或作为独立函数使用。它支持各种参数，如重试次数，重试间隔，重试异常和重试异常消息正则表达式。在重试时，可以指定重试次数，重试间隔，重试异常类型和重试异常消息正则表达式。重试间隔可以是数字，元组(最小间隔，最大间隔，乘数)或自定义函数来计算下一个间隔从上一个间隔。重试异常可以是单个异常类型或异常类型的元组。重试异常消息正则表达式用于匹配异常消息。如果重试次数不是1，则装饰函数将重试。如果重试次数是1或装饰函数成功执行，则返回装饰函数的结果。

要使用此函数，可以将其用作装饰器或作为独立函数调用。

1. 作为装饰器使用：

```py3
   from pitricks.utils.retry import retry
   
   @retry(times=3, interval=1, exp=(IOError, ValueError), regex=".*")
   def my_func():
       # 一些代码
```

   在这里，如果引发IOError或ValueError并且其信息与正则表达式“.*”匹配，则`my_func`将以1秒的间隔重试3次。

2. 作为独立函数使用：

```py3
   from pitricks.utils.retry import retry
   
   def my_func():
       # 一些代码
   
   retry(my_func, times=3, interval=1, exp=(IOError, ValueError), regex=".*")
```

   在这里，如果引发IOError或ValueError并且其信息与正则表达式“.*”匹配，则`my_func`将以1秒的间隔重试3次。

您还可以在调用函数时使用关键字参数`times`，`interval`，`exp`，`regex`。

注意：

- `times` : 重试的次数（默认值-1，表示无限重试）
- `interval` : 重试间隔，可以是数字或元组(最小间隔，最大间隔，乘数)，或元组(最小间隔，最大间隔，函数)
- `exp` : 重试的异常，可以是单个异常类或异常类的元组
- `regex` : 匹配异常消息的正则表达式，默认为“.*”。只有匹配正则表达式patten的exp消息才会被捕获。

### reflect.get_args

此函数`get_args`用于获取函数的参数和上层作用域中的变量。

`get_args`需要两个参数：

- `func`: 您要获取参数的函数。
- `del_self`: 表示是否应从返回的参数中删除“self”参数（默认值: True）

`get_args`返回一个包含两个元素的元组：

- 位置参数的列表
- 关键字参数的字典

当您需要用另一个函数包装另一个函数并保留原始函数的参数时，此函数很有用。该函数将检查传入的函数`func`的参数并将它们与上层作用域中的变量匹配，如果所有必需的参数都存在，它将以参数和关键字参数的元组的形式返回它们，否则将引发异常。

```py3
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

### use_pool

使你的对象不用重复地构造和析构, 而是在`__del__`函数中加入提供的对象池.

### relative_import_everywhere.make_parent_top

也可以直接`from pitricks.utils import make_parent_top`

```py3
from pitricks.utils import make_parent_top
make_parent_top(100)
from ..................................................................... import xxx
```

有效避免在相对引用项目中使用`python -m xxx.xxx.xxx`.

如果顶部模块和二级模块名称相同会出问题, 但应该是python的问题?

**谨慎使用, 可能有未知的bug**

## odd_tools

### method_chaining

这是一个工具，可以将`return None`的类函数转换为`return self`，同时保持函数签名不变（使您能够使用代码提示）。

```
Copy code# chain.py
from logging import FileHandler
from threading import Thread

from pitricks.odd_tools.method_chain import chain, clear_tmp_code

clear_tmp_code()
chain(FileHandler)
chain(Thread)
```

运行上面的代码后，您可以从`pitricks.tmp.classes`导入您指定的类。(或者 `from pitricks import tmp_class`)

就像这样：

```py3
import logging

# 太麻烦了
# 您需要将类分配给变量，然后配置它
from logging import FileHandler
file_handler = FileHandler('1', encoding='utf-8')
file_handler.setFormatter(...)
file_handler.setLevel(...)
logging.root.addHandler(file_handler)

# 链接方法
from pitricks.tmp.classes import FileHandler
logging.root.addHandler(FileHandler('1', encoding='utf-8').setFormatter(...).setLevel(...))

# 原始方法
from threading import Thread
t = Thread(target=...)
t.setDaemon(True)
t.start()

# 链接方法
from pitricks.tmp.classes import Thread
Thread(target=...).setDaemon(True).start()
```

这样，您就可以在调用类的函数时连续调用函数，而不需要每次都重新赋值给变量。这使得代码更简洁，更易于阅读。
