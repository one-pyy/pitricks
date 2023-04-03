from setuptools import setup, find_packages
setup(
  name='pitricks',
  version='0.1.3a3',
  author='pyy',
  url='https://github.com/one-pyy/pitricks',
  packages=find_packages(),
  requires=['regex', 'rich', 'nest_asyncio'],
  description='a tool box'
)