.PHONY: dist install test clean docs

dist:
	python setup.py sdist

install:
	pip install lxml sphinx_testing
	python -B setup.py install

test:
	rm -rf out
	python -B setup.py test
	pip install pycodestyle pylint
	find sphinx_tabs -name "*.py" -print0 | xargs -0 pycodestyle
	pylint --rcfile=pylint.cfg sphinx_tabs

clean:
	rm -rf build dist test-output *.egg-info
