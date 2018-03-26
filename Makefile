PYTHON = python2.7

clean_pyc:
	@find . -not \( -path './venv' -prune \) -name '*.pyc' -exec rm -f {} \;

server:clean_pyc
	$(PYTHON) server/server.py

stop:
	$(PYTHON) server/server.py --action stop

client:clean_pyc
	$(PYTHON) client/main.py

check:
	flake8 client/main.py client/net.py
	flake8 server/

deps:
	python2.7 pyqt4 flake8
