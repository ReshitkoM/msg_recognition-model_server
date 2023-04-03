all: install run

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	chmod u+x runTests.sh

run_tests:
	./runTests.sh

run:
	python3 modelServer.py config

