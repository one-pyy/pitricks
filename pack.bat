python setup.py sdist bdist_wheel
twine upload dist/*
rd -r build
rd -r dist 
rd -r pitricks.egg-info