.PHONY: dist install test clean

dist:
	python setup.py sdist

install:
	pip install -r requirements.txt
	python setup.py install

test:
	rm -rf out
	sphinx-build -E -n -W test test-output

clean:
	rm -rf build dist test-output *.egg-info
