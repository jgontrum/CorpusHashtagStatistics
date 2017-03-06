.PHONY: clean

env/bin/python:
	virtualenv env -p python3.5 --no-site-packages
	env/bin/pip install --upgrade pip
	env/bin/pip install wheel

clean:
	rm -rfv bin develop-eggs dist downloads eggs env parts 
	rm -fv .DS_Store .coverage .installed.cfg bootstrap.py
	find . -name '*.pyc' -exec rm -fv {} \; 
	find . -name '*.pyo' -exec rm -fv {} \; 
	find . -depth -name '*.egg-info' -exec rm -rfv {} \; 
	find . -depth -name '__pycache__' -exec rm -rfv {} \;
