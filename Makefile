.PHONY: dist install test clean docs

dist:
	python setup.py sdist

install:
	pip install -r requirements.txt
	pip uninstall -y sphinx-tabs
	python -B setup.py install

test:
	rm -rf out
	python -B setup.py test
	pip install pep8 pylint
	pep8 sphinx_tabs/tabs.py
	pylint --rcfile=pylint.cfg sphinx_tabs/tabs.py

docs:
	rm -rf docs
	sphinx-build -E -n -W example docs
	echo "" > docs/.nojekyll

clean:
	rm -rf build dist test-output *.egg-info
