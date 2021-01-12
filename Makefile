XARGS := xargs -0 $(shell test $$(uname) = Linux && echo -r)

all:
	@echo "\nThere is no default Makefile target right now. Try:\n"
	@echo "make clean - reset the project and remove auto-generated assets."
	@echo "make test - run the test suite."
	@echo "make coverage - view a report on test coverage."
	@echo "make check - run all the checkers and tests."
	@echo "make package - create a deployable package for the project."
	@echo "make publish - publish the project to PyPI."

clean:
	rm -rf build
	rm -rf dist
	rm -rf nudatus.egg-info
	rm -rf .coverage
	rm -rf .tox
	find . \( -name '*.py[co]' -o -name dropin.cache \) -print0 | $(XARGS) rm
	find . \( -name '*.bak' -o -name dropin.cache \) -print0 | $(XARGS) rm
	find . \( -name '*.tgz' -o -name dropin.cache \) -print0 | $(XARGS) rm

test: clean
	py.test

coverage: clean
	py.test --cov-report term-missing --cov=nudatus tests/

tidy: clean
	black --check *.py
	# Don't reformat test data
	black --check tests/test_*.py

black: clean
	black --check *.py
	black --check tests/test_*.py

check: clean black coverage

package: check
	python setup.py sdist

publish: check package
	@echo "\nChecks pass, good to publish..."
	twine upload dist/*
