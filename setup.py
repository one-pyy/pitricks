from setuptools import setup, find_packages
setup(
  name='pitricks',
  version='0.1.2',
  author='pyy',
  url='https://github.com/one-pyy/pitricks',
  packages=find_packages(),
  requires=['regex', 'rich'],
  description='a tool box'
)