.PHONY: docs
init:
	pip install -r requirements.txt

test:
	tox

test-readme:
	@python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.rst and HISTORY.rst ok") || echo "Invalid markup in README.rst or HISTORY.rst!"

docs:
	cd docs && make html
