from setuptools import setup, find_packages
print(find_packages(where='.'))
setup(
  name='pitricks',
  version='0.0.4',
  author='pyy',
  url='https://github.com/one-pyy/pitricks',
  py_modules=find_packages(where='.'),
  install_requires=[],
  description='python真难Q皿Q'
)