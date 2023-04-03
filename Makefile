all: install run

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run_tests:
	./runTests.sh

run:
	python3 modelServer.py config

