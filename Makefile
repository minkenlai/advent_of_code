PACKAGE=aoc2022

run:
	./run.sh {DAY}

## isort - Run isort to sort the import statements to match pep8 guidelines
isort:
	venv/bin/isort -rc $(PACKAGE) tests

## black - Run the Black auto-formatter
black:
	venv/bin/black $(PACKAGE) tests

## flake8 - Run the flake8 checker
flake8:
	venv/bin/flake8 $(PACKAGE)/ tests/

.PHONY: isort lint black flake8 format run test
