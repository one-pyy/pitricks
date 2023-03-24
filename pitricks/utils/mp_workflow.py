"这个模块还没写完"
from typing import *
import time
from multiprocessing.managers import BaseManager
import multiprocessing as mp
from queue import PriorityQueue
from threading import Lock, Thread
from _thread import LockType
from uuid import uuid4

Require = TypeVar('Require')
Response = TypeVar('Response')
Callback = Callable[[Response], None]
start_time = time.time()

class MyManager(BaseManager):
  pass

class Task(Generic[Require]):
  def __init__(self, data: Require):
    self.data: Require = data
    self.id = uuid4().int
    self.priority = 0.
    self.callback: Optional[Callback] = None
  
  def __lt__(self, other):
    if isinstance(other, Task):
      return self.priority < other.priority
    return NotImplemented


class MPWorkflow(Generic[Require, Response]):
  "这是一个注册到multiprocessing.Manager的优先队列, 也就是说, 我们只能用函数来操作它; 发布任务可以有同步或异步的区别"
  manager = None
  
  @classmethod
  def init(cls) -> 'MPWorkflow':
    if cls.manager is None:
      cls.manager = MyManager()
      cls.manager.start()
    return cls.manager.MPWorkflow() # type: ignore
  
  def __init__(self):
    self.q: PriorityQueue[Task[Require]] = PriorityQueue()
    self.storages: Dict[int, Union[None, Response, Lock]] = {}
  
  def result(self, id: int, timeout: float = 600) -> Tuple[bool, Optional[Response]]:
    "阻塞获取某个任务的结果, 如果[0]为false就是没算好, [1]为None就是出错"
    storage = self.storages.get(id, None) # type: ignore
    if isinstance(storage, LockType):
      if not storage.acquire(timeout=timeout):
        return False, None
      else:
        storage.release()
    # storages[id]已经变成了task ans
    storage: Optional[Response] = self.storages.pop(id, None) # type: ignore
    assert not isinstance(storage, LockType), "bug"
    return True, storage
  
  @overload # 同步, 总是会返回结果
  def publish(self, 
              task: Task[Require], 
              sync: Literal[True] = True,
              *,
              priority: float = 0., 
              timeout: float = 600) -> Tuple[bool, Optional[Response]]: pass
  
  @overload # 异步, 有callback就不会返回结果
  def publish(self, 
              task: Task[Require], 
              sync: Literal[False] = False,
              *,
              priority: float = 0.,
              callback: Callback) -> None: pass
  
  @overload # 异步, 没有callback, 会返回结果
  def publish(self, 
              task: Task[Require], 
              sync: Literal[False] = False,
              *,
              priority: float = 0.,
              callback: None) -> int: pass
  
  def publish(self, 
              task: Task[Require], 
              sync: bool = False,
              *,
              priority: float = 0, 
              timeout: float = 600,
              callback: Optional[Callback] = None):
    "发布任务给worker, priority越高越快; 如果有writer, 则不会返回"
    # 小顶堆, 同时保证越早进入的任务优先级越高(10天够排到一个任务了吧)
    task.priority = -priority+(time.time()-start_time)/864000
    task.callback = callback
    self.q.put(task)
    
    # 同步请求会等待任务完成, 也就是锁释放
    if callback is not None:
      if sync:
        lock = Lock()
        lock.acquire()
        self.storages[task.id] = lock
        return self.result(task.id, timeout)
      else:
        return task.id
  
  def get(self) -> Tuple[int, Require]:
    "获取一个任务"
    task = self.q.get()
    return task.id, task.data
  
  def finish(self, id: int, ans: Optional[Response]):
    "完成一个任务"
    assert id in self.storages, "任务未发布或已完成"
    lock: Lock = self.storages[id] # type: ignore
    self.storages[id] = ans
    lock.release()

MyManager.register('MPWorkflow', MPWorkflow)


# def work(a, b):
#   time.sleep(1)
#   print(a+b)

# def worker(workflow: MPWorkflow):
#   print("hi")
#   while True:
#     id, data = workflow.get()
#     workflow.finish(id, work(*data))

# if __name__=="__main__":
#   a = MPWorkflow.init()
#   p = mp.Process(target=worker, args=(a,)).start()
#   a.publish(Task((1, 2)), sync=True)
#   print("async")
#   a.publish(Task((1, 2)), priority=1)
#   a.publish(Task((2, 2)), priority=2)
#   a.publish(Task((3, 2)), priority=4)
#   a.publish(Task((4, 2)), priority=1, sync=True)
#   print("finish")
#   time.sleep(0.1)