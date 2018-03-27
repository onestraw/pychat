PYTHON = python2.7
PYQT4 = $(shell $(PYTHON) -c "import PyQt4;import os;print(os.path.split(PyQt4.__file__)[0])")

server:clean_pyc
	$(PYTHON) server/server.py

stop:
	$(PYTHON) server/server.py --action stop

client:clean_pyc
	$(PYTHON) client/main.py

pkg:clean
	pyinstaller -n pychat -i client/favicon.ico -p $(PYQT4) -s -w -F -y --clean client/main.py --log-level=DEBUG

check:
	flake8 client/main.py client/net.py --max-line-length=90
	flake8 server/ --max-line-length=90

clean_pyc:
	@find . -not \( -path './venv' -prune \) -name '*.pyc' -exec rm -f {} \;

clean:clean_pyc
	rm -rf build/ dist/ pychat.spec

deps:
	python2.7 pyqt4 flake8 pyinstaller
