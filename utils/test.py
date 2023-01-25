import random
from typing import Literal

__all__ = ['get_random_str']

RANDOM_DICT={
  "digit": """0123456789""",
  "lower": """abcdefghijklmnopqrstuvwxyz""",
  "upper": """ABCDEFGHIJKLMNOPQRSTUVWXYZ""",
  "letter": """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ""",
  "word": """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789""",
  "url": """-_.!~*'()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789""",
  "all": R"""!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ """,
}
def get_random_str(length=10, 
                   mode: Literal["all", "digit", "lower", "upper", "letter", "word", "url"]="all"):
  """ 生成一个指定长度的随机字符串 """
  str_list =[random.choice(RANDOM_DICT[mode]) for _ in range(length)]
  return ''.join(str_list)
